# Extended Page Tables (EPT)

Extended Page Tables (EPT) let an [Intel processor](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) translate the memory addresses that a [guest](guest.md) sees as physical into the physical addresses of the [host](host.md). This is a second stage of address translation. A page table records where a region of memory maps and which types of access it allows.

## Example

An app loads data from a virtual address. The guest's page tables map it to a guest physical address. The CPU then uses EPT to find the corresponding host physical address. The guest kernel can change its page tables, but it does not control EPT. A different guest can use the same guest physical address without using the same host memory.

## Who controls the second mapping?

On a Linux host using [KVM](kernel-based-virtual-machine.md), KVM sets up the second mapping. The CPU enforces its access permissions while the guest runs. See the [KVM memory documentation](https://docs.kernel.org/virt/kvm/x86/mmu.html#translation) for the address translations KVM supports.

[Back to Glossary](../glossary.md)
