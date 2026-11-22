# Network policy

The worker in the [Lamp walkthrough](../design/from-issue-to-patch.md) can build and test without connecting to any network endpoint outside its own environment. The issue tool reads a local example record on the [host](../../glossary/host.md). The [workspace service and artifact collector](workspaces-and-artifacts.md) transfer input and output through a disposable virtual disk before and after the run; neither needs a worker network port.

## Outbound: allow only required destinations

[Egress](../../glossary/egress.md) is network traffic that leaves the worker boundary. The host does not give the Lamp [virtual machine (VM)](../../glossary/virtual-machine.md) a virtual network adapter. The worker gets the compiler, source, and tests at startup, so this design needs no exception. Worker code cannot use the host network to reach the issue store, dependency repositories, other workers, or the control plane.

If a later build needs dependencies, allow a separate fetch service to retrieve approved packages instead of adding egress to the worker. The CI case below shows how to divide those permissions. If the mirror needs authentication, keep it outside the worker as described in [Credentials and identity](credentials-and-identity.md).

If a test variant needs to exercise a client and server together, it can use a loopback endpoint, which is reachable only within that VM. The `LAMP-17` baseline uses no such service.

## Case: a CI job that needs packages

Suppose a [continuous integration (CI) job](../design/deployment-patterns.md#continuous-integration-ci) runs tests for a JavaScript version of Lamp. Unlike `LAMP-17`, it needs packages that are not in the base image. The job needs those package files, not open internet access. Keep the test worker offline and give only the fetch service egress to the approved mirror.

1. **Approve the inputs.** Review the [npm v11.6.2 lockfile](https://github.com/npm/cli/blob/v11.6.2/docs/lib/content/configuring-npm/package-lock-json.md#packages), which records package sources and integrity values. Resolve the full dependency set, not just packages named directly by Lamp. Do not treat changes to the lockfile in an unreviewed patch as permission to fetch new packages.
2. **Fetch without running project code.** Let the fetch service request only the approved archives from `deps.lamp.test`, a fictional dependency mirror that serves copies of approved packages. Keep any mirror [credential](../../glossary/credential.md) in that service. Reject other methods, package paths, and redirects to unapproved destinations. Check each archive against the approved integrity value before staging it.
3. **Install and test inside the boundary.** Give the worker its own staged copy of the package cache. For this case, use packages that do not need install scripts. With a complete cache, [`npm ci`](https://github.com/npm/cli/blob/v11.6.2/docs/lib/content/commands/npm-ci.md#description) can install from the lockfile using [`--offline`](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js#L1353-L1361) and [`--ignore-scripts`](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js#L860-L872). Keep network denial in the worker's boundary: these flags do not control what the tests or their child processes can do.

Check the proposed design with a complete and an incomplete cache. With all approved archives present, the install and tests should succeed. With one missing, the install should fail rather than connect to the registry. Also check that the fetch service rejects an unapproved archive, that it rejects altered bytes for an approved archive, and that the worker cannot connect to the mirror directly. These are acceptance checks for a CI deployment, not results of the local Lamp exercise.

## Inbound: no access unless someone needs a preview

[Ingress](../../glossary/ingress.md) is network traffic that enters across the boundary. Without a virtual network adapter, other environments cannot connect to the worker. The `LAMP-17` run has no preview URL or public port. Reviewers connect only to the separate review store and still need authorization there.

If a later Lamp task needs a browser preview, expose a separate preview service through a gateway that checks the caller's identity and their access to that Lamp session. Route only to the named preview service for the life of the session. Keep the test endpoint and all other worker ports inaccessible from outside. Replies on approved preview connections do not give the worker permission to open new outbound connections. A preview link alone does not grant access.

Use the [access checks](../verification/verifying-access-rules.md) to distinguish expected traffic from traffic that policy should deny. A passing check is evidence for those routes, not proof that every network path is covered.

Next: [Credentials and identity](credentials-and-identity.md) explains how to grant an authorized read without handing a worker a service secret.
