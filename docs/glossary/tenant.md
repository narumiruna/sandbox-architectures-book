# Tenant

A tenant is a user, team, or organization whose work or data a service treats as separate from others. A tenant identifies whose resources and permissions are involved, not what separates running code. One tenant can have many sandbox sessions.

## Example

A build service hosts two teams. One team starts separate [sandboxes](sandbox.md) to build its library and its documentation. The other team starts a sandbox of its own. The first two sandboxes belong to the same tenant, but the third must not be able to read either of their source trees or build results.

## Keeping tenant resources separate

The [control plane](control-plane.md) checks which tenant can start or claim a sandbox and which workspace it attaches. A [tool](tool.md) handler that serves several tenants must also check that the caller's tenant is allowed to use the requested data. It should use identity supplied by the service, not treat a tenant name sent by the script as permission to use that tenant's resources.

A tenant is not necessarily an [isolation unit](isolation-unit.md). The service may give one tenant a separate VM for each job. It must also keep stored output, caches, and restored [snapshots](snapshot.md) within the intended tenant scope. Separate VMs do not fix a shared service that returns another tenant's data.

[Back to Glossary](index.md)
