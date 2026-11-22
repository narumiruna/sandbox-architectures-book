# Verifying access rules

Test that allowed actions succeed and that denied actions fail **because of the rule**. For example, if a worker cannot read a file, first show that the same worker can read it when you expose that file. Otherwise, a typo or a failed launch can look like a successful denial.

## Predict the results

This exercise uses the fictional [Lamp issue workflow](../design/from-issue-to-patch.md). Instead of the virtual machine in the walkthrough, it uses a local [operating-system process sandbox](../../glossary/operating-system-process-sandbox.md). [Bubblewrap 0.11.1](https://github.com/containers/bubblewrap/blob/v0.11.1/README.md) configures the boundary; the Linux [kernel](../../glossary/kernel.md) enforces the [policy](../../glossary/policy.md). The C build uses the host kernel, not a guest kernel.

A [mount](../../glossary/mount.md) makes a host path available inside the worker. A [namespace](../../glossary/namespace.md) gives processes a separate view of a resource. Before running the checks, predict which of these results should change when the runner changes one rule at a time:

| What to check | Expected with the worker policy | Comparison with one rule changed |
| --- | --- | --- |
| Read the assigned input and write the results | The worker reads its Lamp marker, builds and tests the fix in private scratch space, and saves `change.patch` and `test.log` | Not needed for these allowed actions |
| Write into the input copy | The same write returns `EROFS` (read-only filesystem) and creates no file on the host | A writable mount of the same temporary input lets the write succeed |
| Read the other workspace at `/lab/other/marker` | The read returns `ENOENT` (no such file or directory); Cedar is not mounted | Mounting the dummy Cedar workspace makes the same path readable |
| Read a dummy response from a test service on host loopback (`127.0.0.1`) | The connection returns `ECONNREFUSED` (connection refused): there is no listener on that port in the worker's network namespace | With shared networking, the same address and port return `Lamp test service` |

The one-response TCP service binds only to loopback on a port selected by the operating system. It closes when the check ends. No external service or real data is involved. Linux [network namespaces](https://man7.org/linux/man-pages/man7/network_namespaces.7.html) separate interfaces, routes, and port numbers. This comparison tests access to the specified host listener, not an outbound destination list or a production network.

## Run the local checks

Use a non-root account on x86-64 Linux. Install these prerequisites beforehand:

- Bubblewrap with unprivileged user, mount, PID, IPC, UTS, and network namespaces permitted. The exercise was tested with `/usr/bin/bwrap` version 0.11.1. A host or an outer container can block namespace creation.
- A merged `/usr` system, where `/bin`, `/lib`, and `/lib64` point into `/usr`. The sandbox uses `/usr/bin/python3` (tested with Python 3.14.4) and `/usr/bin/gcc` with the system assembler, linker, and C development headers (tested with GCC 15.2.0).
- [uv](https://docs.astral.sh/uv/getting-started/installation/) to run the host script. The command below uses the installed Python, skips project setup, and does not fetch packages.

From the root of your book checkout, run:

```bash
uv run --offline --no-project --python /usr/bin/python3 python -B examples/lamp/lab.py verify
```

Expect eight `PASS` lines, ending with:

```text
PASS: Lamp compiled and passed its test; change.patch and test.log verified
```

Look for **`EROFS`**, **`ENOENT`**, and **`ECONNREFUSED`** with their successful comparisons. A Bubblewrap setup error is a failed experiment, not evidence of a denial. If the host blocks namespaces or lacks the required layout, use a compatible Linux test system. Do not remove an isolation option, change host security settings, or run the example as root to make it pass.

On the [Ubuntu WSL2 test system](measuring-a-sandbox.md#interpret-one-run), all eight checks passed. The runner checked that the input `total.c` was unchanged, that `change.patch` replaced subtraction with addition, and that `test.log` contained `PASS: total(2, 3) = 5`. It discarded the temporary files afterward. The [fixture and runner source](https://github.com/narumiruna/sandbox-architectures-book/tree/main/examples/lamp) are in `examples/lamp/`.

## Interpret the evidence

The successful comparisons show that the files exist and the operations work when allowed. The negative checks show that this configuration gives a worker read-only Lamp input and hides the specified Cedar path. That is not a test of every path, process, or network route. The worker can read the mounted `/usr`, and still shares the host kernel. This lab does not set resource limits or test kernel attack resistance, inherited secrets, VM isolation, or production tenant identity. Use the trusted fixture only. In a real deployment, repeat the checks with the actual runtime, mounts, identity rules, and allowed network destinations. See the [candidate evaluation checklist](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate).

## Check tool authorization separately

The Linux boundary does not decide who may read an issue through a [host tool](../../glossary/host-function.md). Test the [authorization](../../glossary/authorization.md) handler independently. The example below uses synthetic data and the simpler project-wide Lamp grant described in [Tool authorization](../design/tool-authorization.md). It runs outside Bubblewrap and never contacts an issue tracker.

```bash
uv run --offline --no-project --python /usr/bin/python3 python - <<'PY'
issues = {("Lamp", "LAMP-17"): "Incorrect item total", ("Cedar", "CEDAR-9"): "Dummy issue"}


def lookup_as_lamp_reviewer(project, issue):
    if project != "Lamp":
        raise PermissionError(project)
    return issues[project, issue]


if lookup_as_lamp_reviewer("Lamp", "LAMP-17") != "Incorrect item total":
    raise SystemExit("FAIL: expected the Lamp issue")
for project, issue, expected in (("Cedar", "CEDAR-9", PermissionError),
                                 ("Lamp", "CEDAR-9", KeyError)):
    try:
        lookup_as_lamp_reviewer(project, issue)
    except expected:
        continue
    raise SystemExit(f"FAIL: {project}/{issue} should fail with {expected.__name__}")
print("PASS: authorized lookup, project denial, and no cross-project fallback")
PY
```

Next: [Measuring a sandbox](measuring-a-sandbox.md) times the same C workload, without the access probes.
