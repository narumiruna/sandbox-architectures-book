"""Verify access and time the trusted Lamp fixture on a local Linux host."""

import argparse
import socket
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from selectors import EVENT_READ, DefaultSelector
from shutil import copytree
from statistics import median
from tempfile import TemporaryDirectory
from time import perf_counter

from boundary import GUEST_PYTHON, HERE, sandbox_command

TIMEOUT = 10
SAMPLES = 10
LOADED = b"LAMP-17: loaded\n"
PASSED = b"LAMP-17: passed\n"

# Run in the sandbox. A probe reports the kernel error for exactly one operation.
PROBE = """
import errno
from pathlib import Path
import socket
import sys

operation, target = sys.argv[1:]
try:
    if operation == 'read':
        print(Path(target).read_text(encoding='utf-8'), end='')
    elif operation == 'write':
        Path(target).write_text('probe\\n', encoding='utf-8')
        print('OK')
    elif operation == 'connect':
        with socket.create_connection(('127.0.0.1', int(target)), timeout=2) as sock:
            with sock.makefile('r', encoding='utf-8') as response:
                print(response.read(), end='')
    else:
        raise SystemExit(f'unknown probe: {operation}')
except OSError as error:
    print(errno.errorcode.get(error.errno, str(error)))
"""


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def workspace(root):
    input_dir = root / "input"
    output_dir = root / "output"
    copytree(HERE / "input", input_dir)
    output_dir.mkdir()
    return input_dir, output_dir


def check_artifacts(output_dir):
    require(
        {path.name for path in output_dir.iterdir()} == {"change.patch", "test.log"},
        "expected exactly change.patch and test.log",
    )
    patch = (output_dir / "change.patch").read_text(encoding="utf-8")
    require(
        patch.startswith("--- a/total.c\n+++ b/total.c\n")
        and '-    printf("%d\\n", left - right);\n' in patch
        and '+    printf("%d\\n", left + right);\n' in patch,
        "change.patch does not contain the expected fix",
    )
    require(
        (output_dir / "test.log").read_text(encoding="utf-8")
        == "PASS: total(2, 3) = 5\n",
        "unexpected test.log",
    )


def verify(root):
    input_dir, output_dir = workspace(root)
    other_dir = root / "other"
    other_dir.mkdir()
    (input_dir / "marker").write_text("Lamp fixture\n", encoding="utf-8")
    (other_dir / "marker").write_text("Cedar fixture\n", encoding="utf-8")

    def expect_probe(message, expected, operation, target, **policy):
        argv = sandbox_command(
            input_dir,
            output_dir,
            *GUEST_PYTHON,
            "-c",
            PROBE,
            operation,
            target,
            **policy,
        )
        actual = subprocess.check_output(
            argv, stdin=subprocess.DEVNULL, text=True, timeout=TIMEOUT
        )
        require(
            actual == expected + "\n",
            f"{message}: expected {expected!r}, got {actual!r}",
        )
        print(f"PASS: {message} [{expected}]")

    expect_probe("read the Lamp marker", "Lamp fixture", "read", "/lab/input/marker")
    expect_probe(
        "read Cedar with its fixture mounted (control)",
        "Cedar fixture",
        "read",
        "/lab/other/marker",
        visible_other=other_dir,
    )
    expect_probe(
        "Cedar is absent without that mount", "ENOENT", "read", "/lab/other/marker"
    )

    expect_probe(
        "write to read-only input is denied", "EROFS", "write", "/lab/input/new"
    )
    require(not (input_dir / "new").exists(), "read-only probe changed the host input")
    expect_probe(
        "write to the same temporary input with a writable mount (control)",
        "OK",
        "write",
        "/lab/input/new",
        writable_input=True,
    )
    require(
        (input_dir / "new").read_text(encoding="utf-8") == "probe\n",
        "control did not write",
    )
    (input_dir / "new").unlink()

    # One test response on IPv4 loopback; no public listener or real data.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as host_socket:
        host_socket.bind(("127.0.0.1", 0))
        host_socket.listen(1)
        host_socket.settimeout(TIMEOUT)
        port = str(host_socket.getsockname()[1])
        expect_probe(
            "host loopback service is unreachable in the separate network namespace",
            "ECONNREFUSED",
            "connect",
            port,
        )

        def serve_one():
            connection, _ = host_socket.accept()
            with connection:
                connection.settimeout(2)
                connection.sendall(b"Lamp test service\n")

        with ThreadPoolExecutor(max_workers=1) as pool:
            served = pool.submit(serve_one)
            expect_probe(
                "read the same service with shared networking (control)",
                "Lamp test service",
                "connect",
                port,
                shared_network=True,
            )
            served.result()

    output = subprocess.check_output(
        sandbox_command(input_dir, output_dir),
        stdin=subprocess.DEVNULL,
        timeout=TIMEOUT,
    )
    require(output == LOADED + PASSED, "unexpected Lamp stdout")
    check_artifacts(output_dir)
    require(
        (input_dir / "total.c").read_bytes()
        == (HERE / "input" / "total.c").read_bytes(),
        "the original source changed",
    )
    print("PASS: Lamp compiled and passed its test; change.patch and test.log verified")


def time_workload(argv):
    start = perf_counter()
    deadline = start + TIMEOUT
    with subprocess.Popen(
        argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=0
    ) as worker:
        try:
            prefix = b""
            with DefaultSelector() as selector:
                selector.register(worker.stdout, EVENT_READ)
                while b"\n" not in prefix:
                    if not selector.select(max(0, deadline - perf_counter())):
                        raise subprocess.TimeoutExpired(argv[0], TIMEOUT)
                    chunk = worker.stdout.read(4096)
                    if not chunk:
                        break
                    prefix += chunk
            first = perf_counter()
            rest, _ = worker.communicate(timeout=max(0, deadline - perf_counter()))
            done = perf_counter()
        finally:
            if worker.poll() is None:
                worker.kill()
    require(
        worker.returncode == 0 and prefix + rest == LOADED + PASSED,
        f"timed Lamp launch failed (status {worker.returncode}, stdout {prefix + rest!r})",
    )
    return (first - start) * 1000, (done - start) * 1000


def measure(root):
    samples = []
    for index in range(1, SAMPLES + 1):
        sample = root / str(index)
        input_dir, output_dir = workspace(sample)
        samples.append(time_workload(sandbox_command(input_dir, output_dir)))
        check_artifacts(output_dir)
    print(f"{SAMPLES} sequential launches; fresh workspaces; host caches uncontrolled")
    print("run  first_output_ms  completion_ms")
    for index, (first, done) in enumerate(samples, 1):
        print(f"{index:3} {first:16.2f} {done:14.2f}")
    for label, values in zip(("first_output_ms", "completion_ms"), zip(*samples)):
        print(
            f"{label}: min={min(values):.2f} median={median(values):.2f} max={max(values):.2f}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exercise", choices=("verify", "measure"))
    args = parser.parse_args()
    require(sys.platform == "linux", "this fixture requires Linux")
    try:
        with TemporaryDirectory(prefix="lamp-") as directory:
            exercise = verify if args.exercise == "verify" else measure
            exercise(Path(directory))
    except subprocess.CalledProcessError as error:
        raise SystemExit(
            f"FAIL: sandbox launch or fixture exited with status {error.returncode}; "
            "see the diagnostic above"
        ) from None
    except subprocess.TimeoutExpired:
        raise SystemExit(
            f"FAIL: launch or fixture exceeded {TIMEOUT} seconds"
        ) from None
    except OSError as error:
        raise SystemExit(f"FAIL: {error}") from None


if __name__ == "__main__":
    main()
