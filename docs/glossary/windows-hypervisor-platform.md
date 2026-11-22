# Windows Hypervisor Platform (WHP)

Windows Hypervisor Platform (WHP) is a Windows programming interface that lets a [virtual machine monitor (VMM)](virtual-machine-monitor.md) use the host's hardware virtualization support. WHP is the interface on the [host](host.md), not the VMM, the underlying [hypervisor](hypervisor.md), or the kernel running inside the VM.

## Example

A test service uses NVX on Windows to run a Linux [microVM](microvm.md) sandbox. The host-side VMM uses WHP to run the VM. Test programs inside the sandbox still ask the Linux [guest kernel](guest.md) to open files and start programs, not the Windows API.

## What the Windows interface provides

The [Microsoft WHP API](https://learn.microsoft.com/en-us/virtualization/api/) lets a host program create a *partition* (an isolated environment for a guest), configure its memory, and create and run virtual processors. The [API definitions](https://learn.microsoft.com/en-us/virtualization/api/hypervisor-platform/hypervisor-platform) document these operations and how callers can check platform capabilities. The VMM still supplies the VM's configuration and device behavior.

For example, the [NVX Windows/WHP requirements at revision `42f413d`](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#windows--whp) call for enabling hardware virtualization in the host firmware, enabling the Windows Hypervisor Platform feature in Windows, and rebooting. Do not confuse this API with the Linux host interfaces [KVM](kernel-based-virtual-machine.md) and [MSHV](microsoft-hypervisor.md).

[Back to Glossary](../glossary.md)
