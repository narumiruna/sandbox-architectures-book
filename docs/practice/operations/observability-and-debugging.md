# Observability and debugging

Start with the last step that succeeded. A worker that never became ready, an action blocked by an access rule, and a compiler that ran but returned an error need different fixes. [Observability](../../glossary/observability.md) means having enough evidence to tell those cases apart. A single status such as `failed` is not enough.

Use the [Lamp example](../design/from-issue-to-patch.md) to trace a run across the issue lookup, worker setup, build, and cleanup.

## Match the evidence to the layer

The [control plane](../../glossary/control-plane.md) records when a run is requested, ready, and stopped, plus a separate cleanup status. The [runtime](../../glossary/runtime.md) reports command results and execution limit events. The tool handler records issue access decisions; the collector records whether export succeeded. Use non-secret request and attempt IDs to link these records. Record UTC timestamps for the timeline and elapsed time from a clock that does not jump for durations.

The following are three separate fictional attempts. The timestamps and log excerpts only show how to read the evidence.

| Attempt and UTC status | Redacted evidence | Responsible layer and next check |
| --- | --- | --- |
| A1: `10:00:00 provisioning` → `10:00:30 timed_out` | `workspace_attach_timeout`; no `ready` event. | Control plane and workspace service: check why the approved copy could not attach. Verify cleanup of partial allocations. |
| A2: `10:01:00 lookup` → `10:01:01 access_denied` | The issue handler denies a synthetic request outside the Lamp scope before reading a record. | Issue handler owner: verify the run's scope. Do not relax the rule to make the check pass. |
| A3: `10:02:00 ready` → `10:02:02 build_failed` | `compile_failed`; exit `1`. Tests did not run. | The requester can reproduce the build on an approved copy to diagnose the error. No draft patch or raw compiler log is retained. |

A denied action is an event, not necessarily the final session result. Check which command ran next before attributing a later failure to the denial. For a possible [resource limit](resource-limits.md), look for an explicit limit event from the enforcing layer rather than guessing from an exit code.

## Keep diagnostic records safe

Keep only safe metadata: run and attempt IDs, timestamps, stage, status, and reason codes. Do not log environment dumps, raw arguments, issue text, [credential](../../glossary/credential.md) values, or workspace contents. Access is limited to operators assigned to the tenant. The service operator keeps the cleanup record until removal is confirmed, then expires the diagnostic records for the attempt after 30 days. A `cleaned_up` event confirms worker cleanup, not deletion of accepted review files or diagnostic records.

Return to the [decision record](../design/from-issue-to-patch.md#fill-in-your-decision-record) to name the owner and expiry for each copy. Then use [Verifying access rules](../verification/verifying-access-rules.md) to test that allowed actions succeed and forbidden actions fail for the expected reason.
