# Network policy

Give the worker only the network paths the job needs. In this illustrative design, the Linux worker for `LAMP-17` can compile and test Lamp's small C program without reaching anything outside its own environment. The read-only issue tool retrieves the report separately, and the worker returns a patch and test output through the [artifact collector](workspaces-and-artifacts.md), not through a network service of its choice.

## Outbound: allow only required destinations

[Egress](../../glossary/egress.md) is traffic that leaves the worker boundary. Start by denying outbound connections. The Lamp worker gets the compiler, source, and tests at startup, so the baseline needs no exception. The host enforces the rules outside the worker so code running inside cannot change them.

If a later build needs a dependency, allow only the fetch of the declared package from `deps.lamp.test`, a fictional dependency mirror (a service that serves copies of approved packages). A host-controlled fetch service accepts only approved package requests for that mirror and compares the downloaded content with its expected fingerprint before handing it to the worker. The service, not the worker, contacts the mirror. This leaves direct worker egress closed. If the mirror needs authentication, keep it outside the worker as described in [Credentials and identity](credentials-and-identity.md).

Keep host management services, the issue store, other projects, and unrelated network destinations out of reach. Tests that use dummy data do not need those routes. If a test variant needs to exercise a client and server together, start a synthetic test endpoint reachable only within the worker's own network environment. That exchange does not cross the worker boundary.

## Inbound: no access unless someone needs a preview

[Ingress](../../glossary/ingress.md) is traffic that enters across the boundary. Deny new inbound connections by default. The Lamp test endpoint stays private to the worker. A service collecting text results does not need to expose a worker port to reviewers.

If a later Lamp task needs a browser preview, expose a separate preview service through a gateway that checks the caller's identity and their access to that Lamp session. Route only to the named preview service for the life of the session. Keep the test endpoint and all other worker ports inaccessible from outside. Replies on approved preview connections do not give the worker permission to open new outbound connections. A preview link alone does not grant access.

Use the [access checks](../verification/verifying-access-rules.md) to distinguish expected traffic from traffic that policy should deny. A passing check is evidence for those routes, not proof that every network path is covered.
