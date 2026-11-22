# Microsoft Hypervisor (MSHV)

Microsoft Hypervisor is the software that controls how guest operating systems use the physical computer. In this book, *MSHV* denotes the Microsoft Hypervisor backend that a [virtual machine monitor (VMM)](virtual-machine-monitor.md) can access through `/dev/mshv` on a supported Linux host. That device is a host interface, not the [guest kernel](guest.md) or the VMM itself.

## Example

A build service uses NVX to run a Linux [microVM](microvm.md) sandbox on an MSHV-enabled Linux host. The VMM on the host uses `/dev/mshv` to run the VM. Inside it, the build tools still ask the guest's own Linux kernel to open files and run programs.

## Where the Linux interface is available

The [Microsoft Hypervisor specification](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/tlfs) calls its isolated execution environments *partitions*. The *root partition* is the privileged environment that manages the machine and hosts the virtualization stack. The [NVX Linux/MSHV requirements at revision `42f413d`](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#linux--mshv) require Linux to run in that root partition with an MSHV-enabled kernel. That kernel must expose `/dev/mshv`, and the VMM needs read/write access to it. An ordinary Linux guest under the hypervisor does not meet that requirement.

Do not confuse this Linux backend with [Windows Hypervisor Platform (WHP)](windows-hypervisor-platform.md), the host API that a VMM can use on Windows, or with [KVM](kernel-based-virtual-machine.md), a different Linux host interface.

[Back to Glossary](index.md)
