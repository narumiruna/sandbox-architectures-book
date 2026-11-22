# Measuring a sandbox

Measure a whole task, not just how fast a sandbox starts. A worker can accept commands quickly and still take a long time to prepare its workspace, build the project, or return a result. Compare one change at a time on the same workload.

## Decide what each clock measures

| Measure | Start and stop | What it tells you |
| --- | --- | --- |
| Time to first usable command | From local launch to the first line emitted by a command inside the worker | How long the caller waits before the worker can do anything useful |
| End-to-end time | From local launch to the exit of the build-and-test command | What the caller waits for in this fixture; there is no remote queue or artifact upload here |
| Peak memory | [Maximum resident set size (RSS)](https://www.gnu.org/software/time/manual/html_node/Memory-Resources.html) as reported by GNU `time` for the timed launcher | A process high-water mark, not the peak for the worker as a whole; process accounting may not cover all sandbox descendants |
| Cache state | Record what was prepared or reused before each run | Whether two timings include the same setup work |

A [cold start](../../glossary/cold-start.md), an assignment from a warm pool, and a snapshot restore overlap but do not do identical work. Compare their launch paths separately. For a hosted service, also record whether the start time includes queueing and whether the end time includes artifact transfer. See [Sandbox lifecycle](../operations/sandbox-lifecycle.md) for the state that can be reused.

## Run a small local example

This measures the corrected version of the fictional [Lamp task](../design/from-issue-to-patch.md). It compiles a small C program and checks the output. The local lab uses an [operating-system process sandbox](../../glossary/operating-system-process-sandbox.md), not the VM in the example design. Run it from this book's checkout on a Linux system with `uv`, Bubblewrap, GNU `time`, and GCC available in `/usr`. The example assumes a merged `/usr` layout as used on the Ubuntu x86-64 test host, where both `/lib` and `/lib64` resolve under `/usr`. The [Bubblewrap 0.11.1 README](https://github.com/containers/bubblewrap/blob/v0.11.1/README.md) explains how its arguments define the sandbox environment.

```bash
uv run --locked python - <<'PY'
from pathlib import Path
from statistics import median
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory
from time import perf_counter

samples = []
for _ in range(5):
    with TemporaryDirectory() as directory:
        workspace = Path(directory) / 'work'
        workspace.mkdir()
        rss = Path(directory) / 'peak-rss'
        (workspace / 'lamp.c').write_text(
            '#include <stdio.h>\n'
            'int main(void) { printf("%d\\n", 2 + 3); return 0; }\n'
        )
        start = perf_counter()
        with Popen([
            '/usr/bin/time', '-f', '%M', '-o', str(rss),
            'bwrap', '--clearenv', '--setenv', 'PATH', '/usr/bin',
            '--unshare-net', '--unshare-pid', '--new-session', '--die-with-parent',
            '--ro-bind', '/usr', '/usr', '--symlink', 'usr/lib', '/lib',
            '--symlink', 'usr/lib64', '/lib64', '--symlink', 'usr/bin', '/bin',
            '--tmpfs', '/tmp', '--bind', str(workspace), '/work', '--chdir', '/work',
            '/usr/bin/sh', '-ec',
            'printf "ready\\n"; gcc lamp.c -o lamp; test "$(./lamp)" = 5',
        ], stdout=PIPE, text=True) as process:
            line = process.stdout.readline()
            ready = perf_counter()
            status = process.wait()
            done = perf_counter()
        if status or line != 'ready\n':
            raise SystemExit(f'fixture did not complete: {status=}, {line=}')
        samples.append(((ready - start) * 1000, (done - start) * 1000,
                        int(rss.read_text())))

print(f'{len(samples)} launches; fresh workspace; host caches not flushed')
for label, values in zip(('ready_ms', 'done_ms', 'peak_rss_kib'), zip(*samples)):
    print(f'{label}: median={median(values):.1f}, '
          f'min={min(values):.1f}, max={max(values):.1f}')
PY
```

## Interpret one run

One local run on Ubuntu 26.04.1 in WSL2 (Linux 6.18.33.2, x86-64, AMD Ryzen 9 7950X3D; Bubblewrap 0.11.1 and GCC 15.2.0) produced the following. These are five sequential launches, each with a new workspace, no build cache, and host caches left in their normal state.

| Measure | Median | Min–max |
| --- | ---: | ---: |
| Time to first command | 5.4 ms | 4.6–5.9 ms |
| End-to-end time | 34.7 ms | 31.3–64.7 ms |
| Launcher peak RSS | 2,196 KiB | 2,160–2,204 KiB |

This is an example of the method, not a performance baseline. The [launcher RSS](../../glossary/resident-set-size.md) is not total worker peak memory. To measure the latter, use a dedicated [control group](../../glossary/control-group.md) or equivalent backend accounting. This fixture also does not measure warm-pool assignment or snapshot restore. Do not flush the host cache to simulate a cold worker: it is a different thing, and it affects unrelated processes.
