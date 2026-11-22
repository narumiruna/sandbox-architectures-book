# Guest

A guest is the operating system and programs running inside a [virtual machine](virtual-machine.md). Its *guest [kernel](kernel.md)*, the core of that operating system, manages the processors, memory, and devices that the VM presents. It is distinct from the [host](host.md) operating system and its kernel.

## Example

A sandbox runs tests inside a Linux guest. When a test opens a file, it asks the guest kernel, just as it would on a physical Linux computer. If the file is on a virtual disk backed by a host file, the guest still sees a disk, not the directory where the host keeps that file.

## What the guest controls

Guest programs make [system calls](system-call.md) to the guest kernel. The guest kernel manages programs and files inside the VM. The [hypervisor](hypervisor.md) and [virtual machine monitor](virtual-machine-monitor.md) handle different parts of providing the virtual hardware. For example, [Firecracker v1.11.0's design](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md) describes virtual block devices backed by host files.

An administrator inside the guest does not automatically have administrator rights on the host. Still, any host file, network service, or other resource deliberately exposed to the guest must have its own access controls. Workloads in the same VM share the guest kernel; check the [isolation unit](isolation-unit.md) if those workloads must be separate.

[Back to Glossary](index.md)
