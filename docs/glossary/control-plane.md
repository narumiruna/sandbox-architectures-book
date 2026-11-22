# Control plane

A control plane is the part of a system that manages execution environments. It decides things such as where a sandbox runs and when it starts or stops. It can select and configure the mechanism that restricts code, but it is not itself that mechanism.

## Example

A build service receives a request for a fresh [sandbox](sandbox.md). Its control plane starts a [virtual machine](virtual-machine.md) from an approved configuration, assigns it to the request, and removes it when the build ends. While the build runs, the VM boundary limits what the build processes can reach; the management service does not handle each file read.

## Management versus execution

The control plane can choose the execution [runtime](runtime.md), request a particular workspace, and track whether the environment is ready. [Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/README.md), for example, provides a management API on top of Kubernetes for defining and claiming sandboxes. The runtime supplies the [isolation boundary](isolation-boundary.md), so the same kind of management request does not imply the same kind of isolation.

Management still affects security. The service must authorize who can create or claim an environment and whose files it attaches. An execution boundary cannot correct a control plane that assigns the wrong [tenant](tenant.md)'s workspace to a sandbox.

[Back to Glossary](../glossary.md)
