# Measuring a sandbox

Record when the caller sees the first output **and** when the work finishes. A worker may respond quickly but still take much longer to compile, test, and write the result. Before comparing times, [verify the access rules](verifying-access-rules.md); a fast worker that cannot enforce a requirement is not a candidate.

## Use the same workload each time

A [workload](../../glossary/workload.md) is the code and processes the sandbox runs. This exercise uses the [Lamp task](../design/from-issue-to-patch.md) from the access checks. It fixes the subtraction bug in a copy of `total.c`, builds the C program with GCC, checks that two plus three is five, and writes a patch and test log. It runs the same fixture in the same [Bubblewrap process sandbox](../../isolation/native-programs/operating-system-process-sandboxes.md) every time, with no service calls or artificial delays.

| Measure | When the clock stops |
| --- | --- |
| Time to first output | When the caller receives `LAMP-17: loaded`. The worker emits this line after reading the fixture and before compiling or testing the fix. |
| Time to completion | When the caller has drained the worker's output and observed its exit. A successful run has built the program, run its test, and written `change.patch` and `test.log`. |

Both clocks start just before the host launches Bubblewrap, so both include creating the process sandbox and starting Python. The clocks **exclude** staging the input and output directories before launch, checking the artifacts and deleting the workspace afterward, and any remote queue or artifact transfer. In a deployment, measure those stages as well if they contribute to the user's wait.

## Run ten fresh launches

Use the Linux, Bubblewrap, Python, GCC, and `uv` prerequisites listed in [Verifying access rules](verifying-access-rules.md#run-the-local-checks). From the root of your book checkout, run:

```bash
uv run --offline --no-project --python /usr/bin/python3 python -B examples/lamp/lab.py measure
```

Expect ten rows of paired times in milliseconds (`first_output_ms` and `completion_ms`), followed by the minimum, median, and maximum for each measure. The runner requires a zero exit status, both expected output lines, and the expected patch and log on every launch. A failed run stops the exercise instead of reporting a time for that launch.

Each launch uses a new input copy, output directory, and sandbox. There is no persistent build cache, and nothing flushes or tracks the host filesystem cache. Later launches can reuse cached reads of the compiler or libraries. A fresh sandbox does not mean a cold host cache. If you compare another candidate, record the host, kernel, tool versions, runtime policy, concurrency, and how you prepared or reused its workspace and caches.

## Interpret one run

One set of ten sequential runs on Ubuntu 26.04.1 LTS in WSL2 (Linux 6.18.33.2, x86-64, AMD Ryzen 9 7950X3D, host temporary files on `tmpfs`) used Bubblewrap 0.11.1, Python 3.14.4, and GCC 15.2.0. The runner created fresh workspaces. The access checks ran before this sample; nothing flushed or tracked the host caches.

| Measure | Median | Min–max |
| --- | ---: | ---: |
| Time to first output | 24.37 ms | 21.49–26.48 ms |
| Time to completion | 62.23 ms | 58.47–63.94 ms |

The caller saw the first line well before the result was complete. The ranges show why one launch is not enough to characterize even this small task. This is an example of the method, not a performance baseline or a product ranking.

For a real candidate, keep the workload fixed and explain what the launch includes: a [cold start](../../glossary/cold-start.md), an assignment from a [warm pool](../../glossary/warm-pool.md), and a [snapshot](../../glossary/snapshot.md) restore do not do identical work. This example does not measure any VM or warm pool, memory, disk usage, startup under load, or artifact transfer. To measure peak worker memory, use a dedicated [control group](../../glossary/control-group.md) or equivalent backend accounting, not one process's peak [resident set size](../../glossary/resident-set-size.md). See [Sandbox lifecycle](../operations/sandbox-lifecycle.md) for state a service can reuse and the [candidate evaluation checklist](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate) for what else to compare.

Next: [Grow a sandbox service](../operations/scaling-a-sandbox.md) compares queue times and rehearses a cutover with two test tenants.
