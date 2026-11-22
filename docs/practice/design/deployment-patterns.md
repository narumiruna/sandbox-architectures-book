# Deployment patterns

Where a sandbox runs tells you who operates it, not what it isolates. In these illustrative layouts, the same read-only tool retrieves Lamp issue `LAMP-17`, and a separate Linux worker fixes the wrong total in a tiny C program. It compiles and tests a copy, then returns a text patch and test output for review. It cannot publish in any of the four layouts.

## What stays the same

The Linux worker gets a disposable source copy, not a writable mount of the original repository. The issue tool reads a fictional fixture and uses no service credentials. The owners named below would hold any issue-read credentials outside both the script and the worker. Any publication authority belongs to a separate role outside this workflow. Keep the returned patch and logs in review storage with access limited to reviewers and an explicit expiry.

## Who operates each layout?

### Local workstation

The developer operates both the script runtime and the Linux runtime, and owns the issue tool and any read credentials. A local controller creates the scratch copy, stops the worker, and removes the copy after the run. The developer restricts the review directory and deletes saved output when the review period ends. This layout keeps the workflow on the developer's machine, but the runtime must still keep the worker out of the developer's home directory and original checkout.

### Continuous integration (CI)

The CI operator maintains both runtimes on the runner fleet. The project team selects the source revision, owns the issue tool and any read credentials, and sets who can read artifacts and for how long. The CI job controller stages and deletes the scratch copy, including after failure. The CI artifact store expires saved outputs on the project's schedule. A job can use the project's existing review workflow without inheriting its release permissions.

### Self-hosted service

An internal platform team operates both runtimes and provides per-run scratch storage. The project team owns the source, the issue tool and its read authority, and the review access policy. The platform team's [control plane](../../glossary/control-plane.md) stops failed or expired workers, removes scratch storage, and expires retained outputs according to project policy. The organization controls these runtimes and storage systems, and must also maintain them.

### Managed worker service

The customer runs the script runtime and owns the issue tool and any read credentials. The provider operates the Linux runtime and creates and removes the worker's scratch storage. The customer selects the source copy, controls access and expiry in its own review store, and verifies what the provider removes when a job ends. Ending a job need not delete every separate copy the provider retains.

## Check the boundary separately

A local worker can run in a virtual machine (VM), and a remote worker can share a host kernel. Ask which runtime enforces the [isolation boundary](../../sandbox-isolation-boundaries.md), what crosses it, and who removes each copy afterward. See the [architecture survey](../../agent-sandbox-architectures.md) for example implementations.

Next: Start setting access rules with [Tool authorization](tool-authorization.md), which explains what the issue lookup tool must check even when the script runs inside a sandbox.
