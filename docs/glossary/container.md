# Container

A container is an environment prepared for one or more programs to run in. It gives those programs a filesystem and a set of resources to work with. The word *container* alone does not tell you what separates the programs from the host.

## Example

A code review service starts a container with the compiler and test tools a project needs. A second test job can start its own container from the same [container image](container-image.md). The image supplies the starting files; each running container has its own test processes and may have a separate writable filesystem.

## Where isolation comes from

The [container runtime](container-runtime.md) sets up the environment. In a shared-kernel setup, Linux [namespaces](namespace.md) can give processes separate views of resources, and [control groups](control-group.md) can account for or limit resource use. A runtime can also place containers behind a [user-space kernel](user-space-kernel.md) or run them in a [virtual machine](virtual-machine.md). These approaches can start from the same image but have different [isolation boundaries](isolation-boundary.md).

Check what the runtime shares with the workload. A writable host [mount](mount.md), for example, can let code change host files regardless of how the container was packaged. See [the VM, container, and microVM comparison](../sandbox-isolation-boundaries.md#compare-a-vm-a-container-and-a-microvm).

[Back to Glossary](index.md)
