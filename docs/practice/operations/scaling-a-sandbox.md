# Grow a sandbox service

Add capacity if jobs are waiting for a worker. Change the [isolation boundary](../../glossary/isolation-boundary.md) or [authorization](../../glossary/authorization.md) if the new users and data can no longer safely share what they shared before. These are separate decisions. More workers cannot fix a service that gives one customer another customer's files.

The task stays the same: [look up Lamp issue `LAMP-17`, fix the C program, and return a text patch and test log for review](../design/from-issue-to-patch.md). The worker cannot publish. Here is what changes as more people use the service:

| Stage | What may be shared | What must change before adding users |
| --- | --- | --- |
| Personal project | One developer owns every job. Jobs can use the same read-only compiler installation, but they edit separate disposable copies. | Measure where jobs wait before adding workers. Revisit the boundary if anyone else can supply code, tests, or instructions. |
| Internal service | Trusted teams can share the service and a read-only filesystem with a clean compiler installation. Their private repositories, build outputs, and service credentials are not shared. | Authenticate callers, map each job to its team, and authorize the issue, source, and output independently. Use a fresh [virtual machine (VM)](../../glossary/virtual-machine.md) for each attempt in this design. |
| Customer service | Different customers are different [tenants](../../glossary/tenant.md). Share a read-only base image and verified public dependencies, not writable files, private cache entries, or credentials. | Verify tenant assignment and enforcement before admitting customers. Set per-tenant concurrency limits so that a burst from one customer cannot fill every worker slot. |

## Separate state from execution

Make an inventory of what the old service assumes is local: a source checkout, scratch files, cached dependencies, a credential for issue lookup, and saved patches and logs. Write down which of those the worker needs and which should move outside it. Use the [Lamp decision record](../design/from-issue-to-patch.md#fill-in-your-decision-record) to assign an owner and a cleanup rule to each item.

| Resource | Who controls it in the pilot | Lifetime and sharing |
| --- | --- | --- |
| Job record | The [control plane](../../glossary/control-plane.md) authenticates the caller, checks membership, assigns the tenant, queues the work, and records attempts. A submitted project or job ID does not establish membership. | Retries keep the job and tenant IDs, but receive fresh attempt IDs. Record status and timings without recording credentials. |
| Workspace and execution | The control plane selects the tenant's source at a fixed revision and attaches a fresh copy to the worker. The VM and its configured [mounts](../../glossary/mount.md) restrict what the worker can access. | Use a new workspace for each attempt. Stop the worker before removing its copy on success, failure, or cancellation. If cleanup fails, quarantine the worker and retry cleanup instead of reassigning it. |
| Identity and dependencies | The issue tool checks the tenant and returns only the fields Lamp needs. The pilot worker builds offline; it gets no [credentials](../../glossary/credential.md). | Keep any issue service credentials outside the worker. Share only clean, read-only public inputs. Authorize private cache entries per tenant if you add them later. |
| Patch and test log | A collector outside the worker accepts the two expected [artifacts](../../glossary/artifact.md) on success. The review store checks the authenticated tenant and review permission on each fetch. | Keep successful outputs until the agreed expiry. Do not publish or transfer incomplete output on cancellation or failure. |

## Rehearse with fake tenants

The local rehearsal uses [Bubblewrap](https://github.com/containers/bubblewrap) for a process worker that still shares the host [kernel](../../glossary/kernel.md). It uses fake identities, an in-memory review store, the same C workload as the [verification exercise](../verification/verifying-access-rules.md), and two trial worker slots instead of one. It checks real workspace visibility and cleanup in this configuration. It does not test a guest kernel, an identity provider, a durable store, or production capacity. Use only the supplied fixtures: the demo collector is not built to handle hostile output.

Use the Linux, Bubblewrap, Python, and C compiler prerequisites listed in [Verifying access rules](../verification/verifying-access-rules.md). Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for the command below. From the repository root, run:

```sh
uv run --offline --no-project --python /usr/bin/python3 python -B examples/rehearse_migration.py
```

1. **Check separation and cleanup.** Both fake tenants run `LAMP-17`. The workspace for each tenant contains a different marker at the same path. Each worker must see its own marker but not the other marker, which the host confirms exists. Each tenant must retrieve its own patch and test log, but the review store must deny the other tenant even when that tenant knows the job ID. The exercise starts an extra worker, cancels it after partial output appears, checks its workspace is gone, and retries in a fresh workspace.
2. **Compare capacity on equal terms.** Run the same twelve jobs in each pool, arriving every 10 ms (100 submissions per second), without waiting for earlier jobs to finish. Both runs use the same fixture and process boundary, with a priming run and no reused workspace or build outputs. Only the worker slot count changes. Queue time is submission to the start of the assigned slot, before setup; p95 is the value at the 95th percentile (the slowest of twelve here). Count completion only when a job returns successfully. The cost model charges $0.06 per slot-hour for all slots during the measured window, divided by successful jobs. It is not a bill and excludes persistent infrastructure, storage, and traffic.
3. **Make the cutover decision.** Before running, the exercise sets these sample targets: p95 queue time at most 400 ms, all twelve jobs successful, and modeled cost at most $0.000020 per successful job. If isolation or cleanup fails, the exercise stops before capacity testing. If the trial misses a target, Cedar is not admitted. If both gates pass, Cedar's new job runs in the trial while a Lamp job already started in legacy stays there until it finishes. The exercise also checks the pause rule: after draining, only Lamp can go back to legacy.

### Example results

In one Linux run (WSL2 x86-64, AMD Ryzen 9 7950X3D, kernel 6.18.33.2, Bubblewrap 0.11.1, GCC 15.2.0), Lamp and Cedar each saw only their own marker and retrieved only their own patch and log. Cancelling the extra job removed its workspace, and a fresh attempt returned the expected outputs.

| Pool | Median queue | p95 queue | Completed | Modeled cost per success |
| --- | ---: | ---: | ---: | ---: |
| Legacy, one slot | 358.6 ms | 710.6 ms | 12/12 | $0.00000124 |
| Trial, two slots | 117.6 ms | 243.9 ms | 12/12 | $0.00000115 |

More slots were enough to meet the queue target *on this host*. That did not certify the target VM setup or make legacy an acceptable fallback for Cedar. Repeat the checks on your intended setup before accepting customers.

## Switch new jobs in batches

1. Break down the wait before changing the setup. If the queue grows but workers run at the expected speed, try more slots under the same security policy. If environment startup or the build dominates instead, [measure that stage](../verification/measuring-a-sandbox.md) before adding capacity. If a new tenant cannot share the old kernel, mounts, or store permissions, fix those boundaries first even if the queue is empty.
2. Run the fake-tenant checks and retry drill in the target environment, not against live customer data. For the VM design, start with a test control plane and fresh, offline VMs for both test tenants. Where host sharing is allowed, put their VMs on the same test runner and check the workspace and output paths there. Test identity with test accounts at the actual authentication and authorization boundaries. Agree on queue, completion, and cost targets before the pilot. Start with a few approved internal teams, then expand in batches only when the checks and targets hold. Route new jobs to the new environment; let in-flight jobs finish where they started. Do not move running workers or attach an old workspace to a new tenant.
3. Pause admission if an access, cleanup, or capacity gate fails. Route jobs back only if the previous environment still satisfies those jobs' current isolation and authorization requirements. If the old service only supports one owner, it is not a fallback for customer jobs. Hold or reject those jobs until a compliant environment is available.
