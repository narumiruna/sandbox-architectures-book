# Resource limits

[Resource limits](../../glossary/resource-limit.md) control how much a worker can use. Access rules control what it can reach. A disk limit can stop a build from filling storage, but only an access rule keeps the worker away from another project's files.

In the [Lamp example](../design/from-issue-to-patch.md), the worker's budget must cover compiling and testing the C program as well as writing its build files.

## Set a budget and decide what happens at the limit

These example limits are not defaults or measured requirements. Charge usage to the whole worker, including compiler and test processes, not just the first command. The [control plane](../../glossary/control-plane.md) selects budgets, admits work, and enforces deadlines. The [runtime](../../glossary/runtime.md) caps execution resources, and the workspace service limits scratch storage.

| Limit | Example budget | What happens at the limit |
| --- | --- | --- |
| CPU | At most one CPU's worth of execution time over each accounting interval. | The runtime slows the worker instead of stopping it. The cap does not reserve a CPU for Lamp. |
| Memory | 256 MiB of VM memory, shared by Linux and all worker processes. | If the runtime reports a memory limit failure, stop the run. Do not retry unchanged. |
| Disk | 64 MiB for the entire writable `/work` disk, including staged inputs and temporary build files. | Writes beyond the budget fail. If the disk limit causes a build failure, return a safe reason code and discard partial files. |
| Time | 30 seconds each for queue wait, worker startup, and command execution, tracked separately. | Expire a queued request or stop a started attempt at its deadline. Record which phase timed out. |
| Capacity | One allocated worker per [tenant](../../glossary/tenant.md), including provisioning and cleanup; at most two more waiting per tenant. | Queue a request only if space remains. Reject excess requests; never start a second Lamp worker while the first still holds its slot. |

## Do not mistake partial output for success

If Lamp hits its disk limit while linking, a partial binary may exist and tests may never start. For a failed, cancelled, or timed-out attempt, return status and a safe reason code, not the partial patch, raw log, or binary. Record the failing limit only if the enforcing layer reports it. The control plane stops the worker and follows the same [cleanup rules](sandbox-lifecycle.md#what-gets-deleted-and-when) as on success. An authorized requester may start a fresh attempt after fixing the cause; an automatic retry with the same budget may repeat the failure.

The collector separately enforces [output size limits](../data-and-access/workspaces-and-artifacts.md#decide-what-leaves-work). A build and tests can pass but export still fail. Do not publish a partial pair in that case either.

Next: [Observability and debugging](observability-and-debugging.md) explains how to distinguish a limit event from an access denial or failed build.
