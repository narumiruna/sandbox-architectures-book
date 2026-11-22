# Control planes

The [control plane](../../glossary/control-plane.md) decides where a sandbox runs, what it receives, and when to remove it. The [runtime](../../glossary/runtime.md) runs the code inside an [isolation boundary](../../glossary/isolation-boundary.md). Even a strong boundary cannot protect a project if the control plane attaches that project's files to the wrong session.

**Illustrative example:** A read-only tool retrieves issue LAMP-17 in project Lamp: adding two item counts gives the wrong total. A separate Linux worker compiles a tiny C program, runs tests, and returns a text patch and test output for review. It cannot publish.

## From request to cleanup

1. **Authorize and select a policy.** The control plane checks that the requester can start a Lamp [session](../../glossary/sandbox-session.md) with the requested source revision. The [policy](../../glossary/policy.md) tells the runtime which actions are allowed: write to a disposable Lamp copy, use the installed compiler, and return two named outputs. It does not grant access to Cedar or to repository publication. The issue tool checks its own project access independently.
2. **Place and provision the worker.** The control plane picks a host with capacity and support for the required isolation. It asks the runtime to prepare a worker and the workspace service to supply the Lamp copy. The control plane admits commands only after the trusted runtime confirms that the expected workspace and restrictions are in place. If a suitable host is not available, it waits or rejects the request rather than weakening the boundary.
3. **Run and collect.** The runtime enforces the restrictions while the worker compiles and tests. A collector outside the worker accepts only the named, size-limited outputs and hands them to a review store. That store checks reviewer access independently. A patch is text to inspect, not a change to the original checkout.
4. **Stop and verify cleanup.** On success, failure, cancellation, or timeout, the control plane closes command access and requests removal of the worker and its disposable copy. If it cannot confirm removal, it keeps the worker out of reuse and retries cleanup. The review store deletes retained artifacts when its retention period ends.

## Who owns what?

| Component | Responsibility in this example |
| --- | --- |
| Control plane | Authorize the session, select policy and placement, and track readiness and cleanup. |
| Runtime | Run commands inside the boundary, enforce execution restrictions, and report worker start and removal. |
| Issue tool | Authorize the read of LAMP-17; keep its access outside the worker. |
| Workspace service | Supply the approved Lamp revision as a disposable copy and remove it at cleanup. |
| Collector and review store | Validate exports and own reviewer access, retention, and deletion. |

See [Sandbox lifecycle](sandbox-lifecycle.md) for what survives each transition and the [architecture survey](../../agent-sandbox-architectures.md) for implementation examples.
