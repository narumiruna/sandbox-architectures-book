# Virtual machine (VM)

A virtual machine (VM) is a computer environment that presents virtual processors, memory, and devices to its own operating system. That operating system has its own [guest kernel](guest.md). A hardware-backed VM uses processor features to separate guest execution from the [host](host.md), but the sandbox can still give the guest access to selected host resources.

## Example

A build service runs two jobs in separate Linux VMs. Both jobs can install packages in their own guest filesystems. If the service gives both VMs a writable [mount](mount.md) of the same host directory, each job can still affect files the other job uses there.

## What the VM separates

Inside the VM, programs ask the guest kernel for services such as opening files. The [hypervisor](hypervisor.md) controls use of the underlying CPU and memory, while the [virtual machine monitor](virtual-machine-monitor.md) manages the VM and its virtual devices. See [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md#1-hardware-backed-virtual-machines) for how that differs from running processes on the host kernel.

A VM can run one workload or host several [containers](container.md). Those containers can have separate filesystems while still sharing the guest kernel. Check what gets its own VM and which disks, mounts, and network connections the surrounding sandbox exposes.

[Back to Glossary](index.md)
