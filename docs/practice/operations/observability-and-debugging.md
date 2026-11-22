# Observability and debugging

Start with the last step that succeeded. A worker that never became ready, an action blocked by an access rule, and a compiler that ran but returned an error need different fixes. [Observability](../../glossary/observability.md) means having enough evidence to tell those cases apart. A single status such as `failed` is not enough.

Use the [Lamp example](../design/from-issue-to-patch.md) to trace a run across the issue lookup, worker setup, build, and cleanup.

## Match the evidence to the layer

The [control plane](control-planes.md) records when a session is requested, ready, stopped, and cleaned up. The runtime records policy decisions at the execution boundary and reports command results. A build runner identifies whether a result came from the compiler or a test. Use non-secret request and attempt IDs to link these records. Record UTC timestamps for the timeline and elapsed time from a clock that does not jump for durations. Issue tool decisions belong to the tool's own records, not the worker's logs.

The following are three separate fictional attempts. The timestamps and log excerpts only show how to read the evidence.

| Attempt and UTC status | Redacted evidence | Responsible layer and next check |
| --- | --- | --- |
| A1: `10:00:00 requested` → `10:00:03 provision_failed` | `workspace.attach: timeout`; no `ready` event. | Control plane and workspace service: check whether the approved Lamp copy was created and attached before the deadline. Check cleanup of any partial allocation. |
| A2: `10:01:00 ready` → `10:01:01 denied` | A synthetic check records `workspace.read: project not permitted` for Cedar. | Runtime policy enforcement: check the active policy and the project bound to the session. Cedar should remain denied; do not relax the rule to make the check pass. |
| A3: `10:02:00 ready` → `10:02:01 running` → `10:02:02 build_failed` | Compiler exit `1`; `lamp.c:12: expected ';' before 'return'`. Tests did not run. | Build runner and code author: check the indicated line in the draft patch, then rebuild and rerun tests. |

A denied action is an event, not necessarily the final session result. Check which command ran next before attributing a later failure to the denial. For a possible [resource limit](resource-limits.md), look for an explicit limit event from the enforcing layer rather than guessing from an exit code.

## Keep diagnostic records safe

Record only necessary fields, such as status, stage, safe reason code, and a bounded, redacted excerpt. Do not log environment dumps, raw arguments, credential values, or workspace contents. Keep diagnostic records and review outputs access-controlled and expire them under their own retention rules. A `cleaned_up` event confirms worker cleanup, not deletion of retained records.

Next: [Verifying access rules](../verification/verifying-access-rules.md) shows how to test that the right actions succeed and forbidden actions fail for the expected reason.
