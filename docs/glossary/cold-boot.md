# Cold boot

A cold boot starts a new [virtual machine](virtual-machine.md) by booting the operating system inside it instead of resuming saved execution. It can use a prepared disk image; a cold boot does not require installing the operating system from scratch.

## Example

A build service starts a Linux sandbox from a disk image that already contains a compiler. Linux starts inside the VM, and a service inside the VM starts accepting build commands. No compiler process or other running program was carried over from an earlier VM.

## From boot to a usable sandbox

The [virtual machine monitor](virtual-machine-monitor.md) sets up the virtual hardware. The [guest kernel](guest.md) starts, then the guest starts its programs and services. The [NVX library guide at revision `42f413d`](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/library.md#cold-boot) illustrates a cold boot and describes [restore from saved memory and VM state](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/library.md#restore-from-a-snapshot) as a separate path.

Measure boot and readiness separately. The guest may finish booting before the sandbox has attached the project's workspace or can run its first command. A [cold start](cold-start.md) can include a cold boot, but it can also use a [snapshot](snapshot.md) to skip booting the guest.

[Back to Glossary](../glossary.md)
