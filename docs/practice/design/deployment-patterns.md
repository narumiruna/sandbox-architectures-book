# Deployment patterns

Decide where the worker runs and who operates it separately from [what the sandbox isolates](choosing-a-sandbox.md). A worker on remote infrastructure can be self-hosted or managed by a provider. In all four layouts, the same read-only [tool](../../glossary/tool.md) retrieves Lamp issue `LAMP-17`, and a separate Linux worker fixes the wrong total in a tiny C program. It compiles and tests a copy, then returns a text patch and test output for review. It cannot publish.

## What stays the same

The Linux worker gets a disposable [workspace](../../glossary/workspace.md), not a writable [mount](../../glossary/mount.md) of the original repository. The issue tool reads a fictional fixture and uses no service [credentials](../../glossary/credential.md). The owners named below would hold any issue-read credentials outside both the script and the worker. Any publication authority belongs to a separate role outside this workflow. Keep the patch and logs as [artifacts](../../glossary/artifact.md) with access limited to reviewers and an explicit expiry.

## Who operates each layout?

### Local workstation

The developer operates both the script runtime and the Linux runtime, and owns the issue tool and any read credentials. A local controller creates the scratch copy, stops the worker, and removes the copy after the run. The developer restricts the review directory and deletes saved output when the review period ends. This layout keeps the workflow on the developer's machine, but the runtime must still keep the worker out of the developer's home directory and original checkout.

### Continuous integration (CI)

[Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration) (CI) can start a run automatically, but CI is not an isolation mechanism. In this layout, the runner operator maintains the two [runtimes](../../glossary/runtime.md). The project team selects the source revision, owns the issue tool and any read credentials, and sets who can read artifacts and for how long. The CI job controller stages and deletes the scratch copy, including after failure. The CI artifact store expires saved outputs on the project's schedule. A job can use the project's existing review workflow without inheriting its release permissions.

### Self-hosted service

An internal platform team operates both runtimes and provides per-run scratch storage on infrastructure it operates, whether on its premises or in the cloud. Each project team owns its source, the issue tool and its read authority, and its review access [policy](../../glossary/policy.md). The platform team's [control plane](../../glossary/control-plane.md) stops failed or expired workers, removes scratch storage, and expires retained outputs according to project policy. The platform team also has to patch the runtimes, monitor capacity, and handle failures.

### Managed worker service

The customer runs the script runtime and owns the issue tool and any read credentials. The provider operates the Linux runtime and creates and removes the worker's scratch storage. The customer selects the source copy and controls access and expiry in its own review store. The customer must also check what the provider removes or retains, including after cancellation. Ending the job does not necessarily delete separate copies such as logs, caches, or [snapshots](../../glossary/snapshot.md).

## Make three separate decisions

1. **Placement:** Can the approved files leave the workstation or the organization? Record where the job runs and where its state and outputs are stored.
2. **Ownership:** Who patches the runtime, handles failed jobs, verifies cleanup, and pays for capacity? Compare staff time and infrastructure costs for a self-hosted service with provider charges and the work the customer still owns for a managed service.
3. **Execution boundary:** A local worker can use a [virtual machine (VM)](../../glossary/virtual-machine.md); a remote worker can share a [host](../../glossary/host.md) [kernel](../../glossary/kernel.md). Check which runtime enforces the [isolation boundary](../../glossary/isolation-boundary.md), which jobs share it, and what can cross it. See the [architecture survey](../../agent-sandbox-architectures.md) for example implementations.

Next: Start setting access rules with [Tool authorization](tool-authorization.md), which explains what the issue lookup tool must check even when the script runs inside a sandbox.
