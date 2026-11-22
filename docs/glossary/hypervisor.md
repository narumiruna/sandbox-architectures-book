# Hypervisor

A hypervisor is software that controls how [virtual machines](virtual-machine.md) use the physical computer's processors and memory. Some projects use *hypervisor* and *virtual machine monitor* interchangeably. This book uses [virtual machine monitor (VMM)](virtual-machine-monitor.md) for the component that manages the VM and its virtual devices.

## Example

A server runs two test sandboxes in separate VMs. Each VM sees its own virtual processors and memory. The hypervisor lets the two VMs use the same physical machine without giving either guest direct access to the other's memory.

## Virtual execution and access policy

A hardware-backed hypervisor uses processor features to run guest instructions and restrict the physical memory a guest can access. A VMM can use a host interface such as [KVM](kernel-based-virtual-machine.md) to set up this execution and supply device behavior that guest programs rely on. Compare the [Linux KVM API](https://docs.kernel.org/virt/kvm/api.html) and the [Microsoft Hypervisor specification](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/tlfs) for two ways these responsibilities are exposed.

The hypervisor does not decide whether a sandbox should see a project directory or reach an external service. Those decisions depend on what the surrounding system exposes and how it enforces [policy](policy.md).

[Back to Glossary](index.md)
