# Resource limits

[Resource limits](../../glossary/resource-limit.md) control how much a worker can use. Access rules control what it can reach. A disk limit can stop a build from filling storage, but only an access rule keeps the worker away from another project's files.

**Illustrative example:** A read-only tool retrieves LAMP-17: adding two item counts in project Lamp gives the wrong total. A separate Linux worker with an installed compiler builds a tiny C program, runs tests, and returns a text patch and test output for review. It has no access to project Cedar and cannot publish.

## Set a budget and decide what happens at the limit

These example limits are not defaults or measured requirements. The [control plane](control-planes.md) selects them and tracks how many sessions are active. The [runtime](../../glossary/runtime.md) and the storage service enforce the limits that apply to running commands and to scratch storage. Charge usage to the whole session, including compiler and test processes that it starts, not just the first command.

| Limit | Example budget | What happens at the limit |
| --- | --- | --- |
| CPU | Up to one CPU's worth of execution time over each accounting interval. | The runtime slows the job rather than stopping it. The job can still hit the time limit. The cap does not reserve a CPU for Lamp. |
| Memory | 256 MiB for the worker's processes. | In this design, the runtime reports a limit hit and stops the job. The control plane does not retry it unchanged. |
| Disk | 64 MiB for the writable workspace, temporary build files, and session cache combined. | Further writes that would exceed the limit fail. The runner fails the job and discards partial build files during cleanup. |
| Time | 30 seconds elapsed from the first command, including waiting or pauses. | The control plane stops the worker and marks the attempt timed out. It tracks startup with a separate deadline. |
| Concurrent sessions | One allocated worker per project, including provisioning and cleanup. | A second Lamp request waits in a bounded queue or is rejected; it does not start a second worker. |

## Do not mistake partial output for success

If Lamp hits its disk limit while linking, a partial binary may exist, and tests may never start. Record the failing limit if the enforcing layer reported it. Return a short, redacted diagnostic, but do not mark the patch and test output as a completed result. A reviewer can request a fresh run after correcting the cause; an automatic retry with the same budget may just repeat the failure. Limit retained output separately so exporting logs cannot exhaust the review store.

See [Observability and debugging](observability-and-debugging.md) for how to distinguish a limit event from a denial or a failed build.
