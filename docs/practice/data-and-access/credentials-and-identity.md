# Credentials and identity

When a job needs one authorized action, give it that action rather than a [credential](../../glossary/credential.md) (a value that proves identity or grants access). In the [Lamp walkthrough](../design/from-issue-to-patch.md), the host handler reads a local fixture that needs no service credential. The service checks the requester's identity outside the script and worker. Neither program receives the requester's credentials or any credentials for the repository, issue store, or review store.

The collector uses its own service identity to write to the review store. The reviewer uses a separate identity to read the accepted output. Neither identity can publish a fix through this workflow.

## Variant: a remote issue store

If the local fixture later becomes a remote issue store, make the host handler a broker: a trusted component that performs an authorized request on the caller's behalf. The handler uses the identity established by the outer service, not a project name claimed by a script. It makes the request with its own narrow credential and returns only the permitted fields. Hiding the credential would not help if the handler honored any issue request.

Passing a credential through a file or an environment variable would let program code copy it. A short expiry limits how long the credential works; it does not stop copies from ending up in logs or saved state. This variant keeps it in the handler only, not in either runtime's files or environment.

### Follow the placeholder

1. The fictional issue store gives the handler a fake credential represented by `<ISSUE_READ_GRANT>`. The handler is outside both the script and worker boundaries. The grant permits only reading Lamp's `LAMP-17` and expires five minutes after issue. It cannot read Cedar issues, modify issues, or publish repository changes.
2. The handler authorizes the lookup for the caller before using the grant. It rejects unauthorized requests without contacting the store. The store checks the grant's scope and expiry. The handler drops the grant when it expires; a later lookup needs a fresh authorization check and a new grant.
3. Verify that an in-scope lookup works before expiry and that the store rejects the expired grant. Use the fake value to check for leaks in returned issue data, worker settings and files, the patch, test output, and logs (including the handler's logs). Check saved [snapshots](../../glossary/snapshot.md) too, including memory if it was captured. A memory snapshot can hold a copy even after a file is removed. Take worker snapshots before attaching job data, and do not capture the handler's state while it holds credentials.

Next: [Multi-tenant isolation](multi-tenant-isolation.md) shows where to repeat these access checks so Lamp and Cedar cannot read each other's data.
