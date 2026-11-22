# Control plane

A control plane is the part of a system that manages execution environments. It decides things such as where a [sandbox](sandbox.md) runs and when it starts or stops. It can select and configure the mechanism that restricts code, but it is not itself that mechanism.

## Example

A build service receives a request to test Lamp. Its control plane starts a [virtual machine (VM)](virtual-machine.md) from an approved configuration, gives it the Lamp [workspace](workspace.md), and removes it when the run ends. While the tests run, the VM's [guest kernel](guest.md) handles the request to open `total.c`, not the control plane.

## Management versus execution

The control plane can choose the execution [runtime](runtime.md), request a particular workspace, and track whether the environment is ready. [Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/README.md), for example, provides a management API on top of Kubernetes for defining and claiming sandboxes. The runtime supplies the [isolation boundary](isolation-boundary.md), so the same kind of management request does not imply the same kind of isolation.

## When it matters

When many jobs need sandboxes, use the control plane to assign environments and clean up after the jobs. The service must [authorize](authorization.md) who can create or claim an environment and whose files it attaches. An execution boundary cannot correct a control plane that assigns the wrong [tenant](tenant.md)'s workspace to a sandbox. See [Keep packaging, management, and isolation separate](../sandbox-isolation-boundaries.md#keep-packaging-management-and-isolation-separate).

[Back to Glossary](index.md)
