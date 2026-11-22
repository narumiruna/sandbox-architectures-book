# Network policy

The worker in the [Lamp walkthrough](../design/from-issue-to-patch.md) can build and test without connecting to any network endpoint outside its own environment. The issue tool reads a local example record on the [host](../../glossary/host.md). The [workspace service and artifact collector](workspaces-and-artifacts.md) transfer input and output through a disposable virtual disk before and after the run; neither needs a worker network port.

## Outbound: allow only required destinations

[Egress](../../glossary/egress.md) is network traffic that leaves the worker boundary. The host does not give the Lamp [virtual machine (VM)](../../glossary/virtual-machine.md) a virtual network adapter. The worker gets the compiler, source, and tests at startup, so this design needs no exception. Worker code cannot use the host network to reach the issue store, dependency repositories, other workers, or the control plane.

If a later build needs a dependency, allow only the fetch of the declared package from `deps.lamp.test`, a fictional dependency mirror (a service that serves copies of approved packages). A host-controlled fetch service accepts only approved package requests for that mirror and compares the downloaded content with its expected fingerprint before handing it to the worker. The service, not the worker, contacts the mirror. This leaves direct worker egress closed. If the mirror needs authentication, keep it outside the worker as described in [Credentials and identity](credentials-and-identity.md).

If a test variant needs to exercise a client and server together, it can use a loopback endpoint, which is reachable only within that VM. The `LAMP-17` baseline uses no such service.

## Inbound: no access unless someone needs a preview

[Ingress](../../glossary/ingress.md) is network traffic that enters across the boundary. Without a virtual network adapter, other environments cannot connect to the worker. The `LAMP-17` run has no preview URL or public port. Reviewers connect only to the separate review store and still need authorization there.

If a later Lamp task needs a browser preview, expose a separate preview service through a gateway that checks the caller's identity and their access to that Lamp session. Route only to the named preview service for the life of the session. Keep the test endpoint and all other worker ports inaccessible from outside. Replies on approved preview connections do not give the worker permission to open new outbound connections. A preview link alone does not grant access.

Use the [access checks](../verification/verifying-access-rules.md) to distinguish expected traffic from traffic that policy should deny. A passing check is evidence for those routes, not proof that every network path is covered.

Next: [Credentials and identity](credentials-and-identity.md) explains how to grant an authorized read without handing a worker a service secret.
