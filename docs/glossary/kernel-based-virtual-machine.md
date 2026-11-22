# Kernel-based Virtual Machine (KVM)

Kernel-based Virtual Machine (KVM) is a Linux kernel facility for running [virtual machines](virtual-machine.md) using the processor's virtualization features. It gives software on the [host](host.md) an interface to create and run VMs. KVM is neither the [guest kernel](guest.md) nor the full program that manages the VM and its devices.

## Example

A build service runs a Linux sandbox using a [virtual machine monitor (VMM)](virtual-machine-monitor.md) on a Linux host. The VMM uses KVM to run the guest's virtual processors and supplies a virtual disk for the build. The build tools make ordinary Linux requests to the guest kernel, not requests to KVM on the host.

## The host interface

The [Linux KVM API](https://docs.kernel.org/virt/kvm/api.html) describes how the VMM opens `/dev/kvm`, creates a VM and its virtual processors, and sets up guest memory. The VMM can ask which optional features are available because support varies by host.

A VMM needs access to `/dev/kvm` on the host. For example, the [NVX Linux/KVM requirements at revision `42f413d`](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#linux--kvm) call for hardware virtualization and read/write access to the device. That access is for the host-side VMM, not the sandboxed workload. See [MSHV](microsoft-hypervisor.md) and [WHP](windows-hypervisor-platform.md) for other host interfaces.

[Back to Glossary](../glossary.md)
