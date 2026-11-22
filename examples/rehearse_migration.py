"""Rehearse Lamp tenant separation and cutover with dummy data, not a live service."""

import math
import os
import select
import shutil
import signal
import statistics
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path

from lamp.boundary import GUEST_PYTHON, GUEST_WORKLOAD, sandbox_command

INPUT = Path(__file__).resolve().parent / "lamp" / "input"
ARTIFACT_NAMES = ("change.patch", "test.log")
TENANTS = ("lamp", "cedar")
JOB_COUNT = 12
INTERVAL = 0.010
QUEUE_TARGET_MS = 400
COST_TARGET_USD = 0.000020
SLOT_USD_PER_HOUR = 0.06

# The host checks that the other marker exists before passing its path here.
# The sandbox itself maps only the current job's workspace.
CHECK_MOUNTS = """\
import os, pathlib, sys
own = pathlib.Path('/lab/input/tenant-marker.txt').read_text().strip()
assert own == sys.argv[1], own
for other in (sys.argv[2], '/lab/other/tenant-marker.txt'):
    try:
        pathlib.Path(other).read_text()
    except FileNotFoundError:
        pass
    else:
        raise AssertionError(f'other tenant marker was visible at {other}')
print(f'{own}: own marker visible, other workspace not mounted', flush=True)
assert not list(pathlib.Path('/lab/output').iterdir()), 'stale output'
os.execv(sys.argv[3], sys.argv[3:])
"""


class ReviewStore:
    """Model an owner check after authentication; no real identities or credentials."""

    def __init__(self):
        self._records = {}

    def collect(self, tenant, job_id, output):
        self._records[job_id] = (
            tenant,
            tuple((output / name).read_bytes() for name in ARTIFACT_NAMES),
        )

    def fetch(self, caller_tenant, job_id):
        owner, data = self._records[job_id]
        if caller_tenant != owner:
            raise PermissionError("review store denied a different tenant")
        return data


@contextmanager
def workspace(parent, fixture):
    with tempfile.TemporaryDirectory(prefix="job-", dir=parent) as directory:
        job = Path(directory)
        shutil.copytree(fixture, job / "input")
        (job / "output").mkdir()
        yield job


def run_job(parent, fixture, *worker_args, store=None, tenant=None, job_id=None):
    with workspace(parent, fixture) as job:
        output = job / "output"
        subprocess.run(
            sandbox_command(job / "input", output, *worker_args),
            check=True,
            capture_output=not worker_args,
            timeout=10,
        )
        if store is not None:
            store.collect(tenant, job_id, output)
        return job


@contextmanager
def hold_worker(job):
    args = sandbox_command(
        job / "input",
        job / "output",
        *GUEST_PYTHON,
        "-c",
        "import os, sys; from pathlib import Path; "
        "Path('/lab/output/partial').touch(); print('ready', flush=True); input(); "
        "os.execv(sys.argv[1], sys.argv[1:])",
        *GUEST_WORKLOAD,
    )
    with subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        start_new_session=True,
    ) as worker:
        try:
            ready, _, _ = select.select([worker.stdout], [], [], 10)
            assert ready and worker.stdout.readline() == b"ready\n", (
                "worker did not start"
            )
            assert (job / "output" / "partial").is_file() and worker.poll() is None
            yield worker
        finally:
            if worker.poll() is None:
                os.killpg(worker.pid, signal.SIGKILL)
            worker.wait(timeout=10)


def check_cancellation(parent, fixture):
    with workspace(parent, fixture) as job:
        with hold_worker(job) as worker:
            pass  # Cancel instead of releasing the worker to finish.
        assert worker.returncode != 0, "worker finished instead of being cancelled"
    assert not job.exists(), "cancelled workspace remains"
    print(
        "cancelled job: worker stopped, partial output and workspace removed",
        flush=True,
    )
    return job


def check_tenants(root):
    fixtures = {}
    jobs = root / "jobs"
    jobs.mkdir()
    store = ReviewStore()
    for tenant in TENANTS:
        fixtures[tenant] = shutil.copytree(INPUT, root / tenant)
        (fixtures[tenant] / "tenant-marker.txt").write_text(f"{tenant}-fixture\n")
    for tenant, other in (TENANTS, TENANTS[::-1]):
        other_marker = fixtures[other] / "tenant-marker.txt"
        assert other_marker.read_text().strip() == f"{other}-fixture"
        probe = (
            *GUEST_PYTHON,
            "-c",
            CHECK_MOUNTS,
            f"{tenant}-fixture",
            str(other_marker),
            *GUEST_WORKLOAD,
        )
        finished = run_job(
            jobs, fixtures[tenant], *probe, store=store, tenant=tenant, job_id=tenant
        )
        assert not finished.exists()
        patch, log = store.fetch(tenant, tenant)
        assert patch.startswith(b"--- a/total.c\n+++ b/total.c\n")
        assert log == b"PASS: total(2, 3) = 5\n"
        print(f"{tenant}: retrieved own patch and test log", flush=True)
        try:
            store.fetch(other, tenant)
        except PermissionError as error:
            print(f"{other} reading {tenant} artifacts: {error}", flush=True)
        else:
            raise AssertionError("other tenant could retrieve artifacts")
    assert store.fetch("lamp", "lamp") == store.fetch("cedar", "cedar")
    cancelled = check_cancellation(jobs, fixtures["lamp"])
    retried = run_job(
        jobs, fixtures["lamp"], store=store, tenant="lamp", job_id="retry"
    )
    assert retried != cancelled and not retried.exists()
    assert store.fetch("lamp", "retry") == store.fetch("lamp", "lamp")
    print("retry: new workspace, same patch and test log", flush=True)
    return fixtures


def compare_pool(parent, label, slots):
    def execute(submitted):
        started = time.monotonic()
        try:
            run_job(parent, INPUT)
        except (subprocess.SubprocessError, OSError) as error:
            print(f"{label}: failed job: {error}", flush=True)
            return (started - submitted) * 1000, False
        return (started - submitted) * 1000, True

    with ThreadPoolExecutor(max_workers=slots) as pool:
        pending = []
        start = time.monotonic()
        for index in range(JOB_COUNT):
            time.sleep(max(0, start + index * INTERVAL - time.monotonic()))
            pending.append(pool.submit(execute, time.monotonic()))
        results = [future.result() for future in pending]
        elapsed = time.monotonic() - start
    waiting = sorted(delay for delay, _ in results)
    p95 = waiting[math.ceil(0.95 * len(waiting)) - 1]
    passed = sum(ok for _, ok in results)
    cost = slots * elapsed / 3600 * SLOT_USD_PER_HOUR / passed if passed else math.inf
    within_goals = (
        p95 <= QUEUE_TARGET_MS and passed == JOB_COUNT and cost <= COST_TARGET_USD
    )
    print(
        f"{label}: slots={slots}, queue median={statistics.median(waiting):.1f} ms, "
        f"p95={p95:.1f} ms, complete={passed}/{JOB_COUNT}, window={elapsed:.3f} s, "
        f"modeled USD/success={cost:.8f}, goals={'met' if within_goals else 'missed'}"
    )
    return within_goals


def route_job(tenant, pilot_open):
    if pilot_open and tenant in TENANTS:
        return "pilot"
    return "legacy" if tenant == "lamp" else None


def rehearse_cutover(root, fixtures, pilot_ready):
    pools = {name: root / name for name in ("legacy", "pilot")}
    for pool in pools.values():
        pool.mkdir()
    original_route = route_job("lamp", pilot_open=False)
    assert original_route == "legacy" and route_job("cedar", pilot_open=False) is None
    with (
        workspace(pools[original_route], fixtures["lamp"]) as old_job,
        hold_worker(old_job) as worker,
    ):
        if pilot_ready:
            new_route = route_job("cedar", pilot_open=True)
            assert new_route == "pilot"
            run_job(pools[new_route], fixtures["cedar"])
            assert worker.poll() is None and old_job.parent == pools["legacy"]
            print(
                "cutover: new job ran in the pilot while the original stayed in legacy"
            )
        stdout, _ = worker.communicate(input=b"finish\n", timeout=10)
        assert worker.returncode == 0 and b"LAMP-17: passed" in stdout
    assert not old_job.exists()
    assert route_job("lamp", pilot_open=False) == "legacy"
    assert route_job("cedar", pilot_open=False) is None
    print("pause: legacy drained; only the original owner can return to it")


def main():
    print(
        f"Targets: p95 queue <= {QUEUE_TARGET_MS} ms, {JOB_COUNT}/{JOB_COUNT} completed, "
        f"<= ${COST_TARGET_USD:.6f}/success; same {JOB_COUNT} arrivals at "
        f"{1 / INTERVAL:g}/s, all may be in flight.",
        flush=True,
    )
    with tempfile.TemporaryDirectory(prefix="lamp-pilot-") as directory:
        root = Path(directory)
        fixtures = check_tenants(root)
        # Pre-run the same fixture once so neither pool gets the only initial run.
        run_job(root, INPUT)
        compare_pool(root, "legacy", slots=1)
        pilot_ready = compare_pool(root, "pilot", slots=2)
        rehearse_cutover(root, fixtures, pilot_ready)
    print(
        "Rehearsal decision: "
        + (
            "advance the rehearsal; validate target VMs and identity separately"
            if pilot_ready
            else "pause; diagnose the missed targets before adding traffic"
        )
    )


if __name__ == "__main__":
    main()
