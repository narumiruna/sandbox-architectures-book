# Control planes

The [control plane](../../glossary/control-plane.md) decides where a [sandbox](../../glossary/sandbox.md) runs, what it receives, and when to remove it. The [runtime](../../glossary/runtime.md) sets up and runs the code inside an [isolation boundary](../../glossary/isolation-boundary.md). Even a strong boundary cannot protect a project if the control plane attaches that project's files to the wrong run.

In the [Lamp example](../design/from-issue-to-patch.md), the control plane prepares a separate Linux worker to build and test a copy of the source, then removes the worker and its copy.

## From request to cleanup

1. **Authorize and select a policy.** The control plane checks that the requester may start a Lamp [session](../../glossary/sandbox-session.md) for `LAMP-17` and use the requested source revision. It binds those inputs to the run. Its [policy](../../glossary/policy.md) sets requirements for the runtime, workspace service, and collector; those components enforce the requirements. The issue tool still checks its own record access.
2. **Place and provision the worker.** The control plane picks a [host](../../glossary/host.md) with capacity and support for a fresh [virtual machine (VM)](../../glossary/virtual-machine.md). It asks the workspace service for the approved Lamp copy and the runtime for a VM. Before allowing the first command, it checks the reported configuration: correct workspace, clean image, resource limits, and no external network connection. If a requirement cannot be met, wait within the queue deadline or fail the attempt. Do not switch to a weaker setup.
3. **Run, stop, and collect.** The VM confines the running code to the exposed resources. The runtime reports command status, and the control plane stops the worker. Only after a completed, passing build and test run may the collector accept the two named text files. The review store checks reviewer access separately.
4. **Verify cleanup.** The control plane tracks resource removal on every exit path, including partial setup or a failed export. If removal is not confirmed, keep the resources out of use, retry cleanup, and alert the operator. The review store owns expiry of accepted [artifacts](../../glossary/artifact.md); worker cleanup does not expire them.

## Who owns what?

| Component | Responsibility in this example |
| --- | --- |
| Control plane | Bind each run to its [tenant](../../glossary/tenant.md), issue, and revision; select the setup; track readiness, deadlines, and cleanup. |
| Interpreter and VM runtime | The interpreter restricts which operations the script can call. The VM runtime exposes only the configured resources and reports worker status and removal. |
| Issue tool handler | Check access to `LAMP-17` and return only the permitted fields. |
| Workspace service | Supply the approved Lamp copy on the run's disk, enforce the disk budget, and confirm its removal. |
| Collector | Validate the two files from that run's disk and write them to the matching review entry. |
| Review store | Authorize each reviewer read and delete accepted files on expiry. |
| Service operator | Investigate provisioning, capacity, and cleanup failures; use diagnostic records, not the worker's scratch files. |

In this hosted example, the platform team operates the control plane, runtimes, and storage services. The Lamp project owner supplies the issue fixture and decides which callers may run and review Lamp tasks. See [Deployment patterns](../design/deployment-patterns.md) for how these responsibilities change when someone else runs the worker.

Next: [Sandbox lifecycle](sandbox-lifecycle.md) follows what the service keeps and deletes at each transition.
