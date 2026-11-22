# Credentials and identity

When a job needs one authorized action, give it that action rather than a credential it can use elsewhere. In this illustrative design, the read-only issue tool looks up `LAMP-17`, which reports an incorrect total in Lamp. The separate Linux worker gets the task summary and prepared source, compiles the tiny C program, runs the tests, and returns a text patch and test output. It never receives an issue credential or permission to publish.

## Decide where the credential lives

A [credential](../../glossary/credential.md) proves identity or grants access. Passing one into a workload through a file or an environment variable is simple when the workload must contact a service directly. But code that can use the value can also read or copy it. A short expiry limits how long the credential works; it does not prevent copies from ending up in logs or saved state.

A broker is a trusted component that performs an authorized request on the caller's behalf. The issue tool's handler acts as the broker here. It checks who is asking and what they can read, using the identity established by the outer service, not a project name claimed by the caller. It then makes the request with its own narrow credential and returns only the permitted fields. Hiding the credential alone would not help if the handler honored any issue request.

## Follow the placeholder

1. The fictional issue store gives the handler a fake credential represented by `<ISSUE_READ_GRANT>`. The handler is outside both the script and worker boundaries. The grant permits only reading Lamp's `LAMP-17` and expires five minutes after issue. It cannot read Cedar issues, modify issues, or publish repository changes.
2. The handler authorizes the lookup for the caller before using the grant. It rejects unauthorized requests without contacting the store. The store checks the grant's scope and expiry. The handler drops the grant when it expires; a later lookup needs a fresh authorization check and a new grant.
3. Verify that an in-scope lookup works before expiry and that the store rejects the expired grant. Use the fake value to check for leaks in returned issue data, worker settings and files, the patch, test output, and logs (including the handler's logs). Check saved [snapshots](../../glossary/snapshot.md) too, including memory if it was captured. A memory snapshot can hold a copy even after a file is removed. Take worker snapshots before attaching job data, and do not capture the handler's state while it holds credentials.

Pair this design with [tool authorization](../design/tool-authorization.md) and [network policy](network-policy.md): a permitted route is not proof that the caller may perform the action.
