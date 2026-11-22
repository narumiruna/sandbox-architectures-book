# Pod

A pod is the smallest unit that Kubernetes can deploy. It contains one or more [containers](container.md) that run together, share a network environment, and can share storage. A pod does not necessarily have its own kernel: the selected runtime determines the [isolation boundary](isolation-boundary.md).

## Example

A test sandbox runs a web server and a test runner in two containers in the same pod. The test runner can connect to the server on `localhost`. If the service mounts a shared output directory in both containers, both can read test results saved there.

## What sharing a pod means

In the standard model described in the [Kubernetes Pods documentation](https://kubernetes.io/docs/concepts/workloads/pods/), containers in a pod share an IP address and port space. Shared storage must be set up for the containers that need it. A runtime that uses a [virtual machine](virtual-machine.md) can make the pod the [isolation unit](isolation-unit.md). For example, [Kata Containers 4.4.0](https://github.com/kata-containers/kata-containers/blob/4.4.0/docs/design/architecture/README.md#kubernetes-support) puts a Kubernetes pod in a VM. Its containers share the VM's guest kernel; each does not get a separate VM.

[Back to Glossary](../glossary.md)
