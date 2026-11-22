# VM exit

A VM exit is a processor transition from running a [guest](guest.md) to running its [hypervisor](hypervisor.md). A VM exit does not shut down the [virtual machine](virtual-machine.md). The hypervisor can handle the event and resume the guest.

## Example

A guest driver accesses a virtual device. If that access is configured to cause a VM exit, the CPU transfers control to [KVM](kernel-based-virtual-machine.md) on a Linux KVM host. KVM may handle the event in the host kernel or return control to the [virtual machine monitor (VMM)](virtual-machine-monitor.md) to supply the device behavior.

## Different from a guest system call

A [system call](system-call.md) normally changes the [privilege level](cpu-privilege-level.md) from guest app to guest kernel without leaving the guest. A VM exit crosses the guest boundary. On KVM, it is also distinct from the host's [`KVM_RUN`](https://docs.kernel.org/virt/kvm/api.html#kvm-run) call returning to the VMM: some exits are handled and guest execution resumes without that call returning.

[Back to Glossary](index.md)
