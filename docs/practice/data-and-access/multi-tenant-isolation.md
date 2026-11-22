# Multi-tenant isolation

Separate running jobs and check access to the data that outlives them. In the [Lamp walkthrough](../design/from-issue-to-patch.md), Lamp and Cedar are two [tenants](../../glossary/tenant.md): groups whose work and data must stay separate. Cedar must not be able to read Lamp's issue, workspace, or review output, even if it knows the IDs and filenames.

## Decide what shares a boundary

The [isolation unit](../../glossary/isolation-unit.md) is the set of [workloads](../../glossary/workload.md) that share one instance of an [isolation boundary](../../glossary/isolation-boundary.md). Choosing what shares an instance is different from choosing the mechanism. The [architecture survey](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel) compares systems that group work differently even when all use [virtual machines (VMs)](../../glossary/virtual-machine.md).

| One boundary per | Benefit | What can carry over |
| --- | --- | --- |
| Request | Each job can start clean. | Nothing from the previous job inside the boundary if the instance is replaced; external stores still need checks. Setup repeats for every job. |
| Session | Several steps can reuse an editor, workspace, or build output. | Files and processes live across requests in the session. Only callers authorized for that session may reattach. |
| Tenant | Jobs for a tenant can use one long-lived environment. | Without additional boundaries, jobs and users in that tenant share a runtime. This only fits if the jobs may share that state. |

## Keep shared resources deliberate

Lamp starts one fresh VM per build attempt, even for a retry by the same tenant. The [control plane](../../glossary/control-plane.md) binds the tenant and run to the VM based on the requester's verified identity. The workspace service checks that binding before it attaches the run's disposable [workspace](../../glossary/workspace.md) at `/work`. A name like `lamp/work` is a label, not a permission check.

The jobs can share a clean, read-only compiler image. They do not share workspace disks, running VMs, or writable caches (stores that save inputs or build results for later use). This example saves no snapshots after job data is attached. If a later design needs a private cache, its service must check tenant access before it returns an entry.

The issue handler checks tenant, action, and record on each call. The review store checks tenant and the run's reviewer assignment on each read. Lamp membership alone is not enough. Diagnostic records are also tenant-scoped for the operator handling the run. A separate VM cannot prevent one of these stores from handing data to the wrong tenant.

## Check with dummy data

Give Lamp and Cedar dummy workspaces and artifacts with the same filenames but different marker text. Check that each tenant can read its own marker but cannot attach the other workspace or fetch the other artifact. Check that only the permitted Lamp caller can read `LAMP-17`. If private caches exist, put a different marker at the same entry name for each tenant and check that each gets its own value. Start a fresh Cedar job on infrastructure that ran a Lamp job and check that the Lamp marker is absent. See [Verifying access rules](../verification/verifying-access-rules.md) for a local example; these checks do not cover every effect of sharing a host.

Next: In [Control planes](../operations/control-planes.md), see how the service starts a worker, attaches the right tenant's workspace, and verifies cleanup.
