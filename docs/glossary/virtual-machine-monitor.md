# Virtual machine monitor (VMM)

A virtual machine monitor (VMM) is the software that creates or manages a [virtual machine](virtual-machine.md) and presents its virtual devices. Some projects call this software a [hypervisor](hypervisor.md). This book uses *VMM* for VM and device management, not for the whole sandbox service or the operating system running inside the VM.

## Example

A test service starts a VM and asks its VMM to attach a virtual disk. Programs inside the VM ask the [guest kernel](guest.md) to read files. The VMM supplies the virtual disk behavior; it does not receive those programs' requests directly as guest system calls.

## Between the host interface and the guest

For a hardware-backed VM, the VMM configures guest memory and virtual processors through a host virtualization interface. It also provides or connects the virtual devices the guest sees. For example, [Firecracker v1.11.0's design](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md) describes how it uses [KVM](kernel-based-virtual-machine.md) to run virtual processors and presents virtual disks backed by files on the host.

A sandbox [control plane](control-plane.md) can use a VMM to start and stop VMs, but choosing where to run jobs and who gets workspace or network access are separate responsibilities. Check the whole sandbox, not just its VMM, to learn what it exposes.

[Back to Glossary](index.md)
