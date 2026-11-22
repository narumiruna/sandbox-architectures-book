# Multi-tenant isolation

Separate running jobs and check access to the data that outlives them. In this illustrative service, Lamp and Cedar are two [tenants](../../glossary/tenant.md): groups whose work and data must stay separate. The read-only issue tool serves Lamp's `LAMP-17` report to authorized Lamp callers. A separate Linux worker compiles the tiny C program, runs the tests, and returns a text patch and test output to a Lamp reviewer. Cedar must not be able to see any of it, and the worker cannot publish.

## Decide what shares a boundary

The [isolation unit](../../glossary/isolation-unit.md) is the set of workloads that share one instance of a boundary. Choosing what shares an instance is different from choosing the mechanism. The [architecture survey](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel) compares systems that group work differently even when all use virtual machines (VMs).

| One boundary per | Benefit | What can carry over |
| --- | --- | --- |
| Request | Each job can start clean. | Nothing from the previous job inside the boundary if the instance is replaced; external stores still need checks. Setup repeats for every job. |
| Session | Several steps can reuse an editor, workspace, or build output. | Files and processes live across requests in the session. Only callers authorized for that session may reattach. |
| Tenant | Jobs for a tenant can use one long-lived environment. | Without additional boundaries, jobs and users in that tenant share a runtime. This only fits if the jobs may share that state. |

## Keep shared resources deliberate

Use a fresh Linux VM for each build request here. The [control plane](../../glossary/control-plane.md) assigns it to the authenticated tenant and attaches that job's [workspace](workspaces-and-artifacts.md) at `/work`. The service can share a clean, read-only compiler image and verified public dependencies from a cache, a store that avoids fetching the same inputs repeatedly. Jobs cannot change those shared inputs. Private dependency caches and cached build outputs must be separated by tenant if kept at all; the cache service checks tenant access before returning an entry. A naming convention alone does not enforce access.

Keep workspace copies and any snapshots with job data separate. The issue tool and artifact store check the authenticated tenant and applicable permissions on each request, even when a caller knows an issue or artifact identifier. A separate runtime cannot stop an artifact service from giving a file to the wrong caller.

## Check with dummy data

Give Lamp and Cedar dummy workspaces and artifacts with the same filenames but different marker text. Check that each tenant can read its own marker but cannot attach the other workspace or fetch the other artifact. Check that only the permitted Lamp caller can read `LAMP-17`. If private caches exist, put a different marker at the same entry name for each tenant and check that each gets its own value. Start a fresh Cedar job on infrastructure that ran a Lamp job and check that the Lamp marker is absent. See [Verifying access rules](../verification/verifying-access-rules.md) for a local example; these checks do not cover every effect of sharing a host.
