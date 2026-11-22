# Isolation unit

An isolation unit is the set of workloads, or running pieces of work, that share one instance of an isolation boundary. A boundary separates one unit from another at a particular layer. It does not by itself separate workloads inside the same unit.

## Example

A service gives each Kubernetes [pod](pod.md) its own [virtual machine](virtual-machine.md) as a sandbox. One pod contains a test runner and a helper that collects results. They share the same VM and its operating-system kernel. A second pod has a different VM, so the VM boundary separates the pods, not the two programs in the first pod.

## Which layer the unit describes

The [isolation boundary](isolation-boundary.md) tells you *how* work is separated. The unit tells you *which work* is separated by each instance. With a VM per pod the unit is a pod; with a VM per container it is a [container](container.md). See [which workloads share a guest kernel](../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel) for a diagram comparing three implementations.

The same system can have smaller units at another layer. Processes in one VM can have separate filesystem views, but that does not give each process a separate guest kernel. If two [tenants](tenant.md) must not share a guest kernel, check how the [control plane](control-plane.md) places their workloads, not just whether the service uses VMs.

[Back to Glossary](../glossary.md)
