# CPU privilege level

A CPU privilege level determines which operations code can do directly on the processor. On x86-64, the [operating-system kernel](kernel.md) normally runs at ring 0, the most privileged level, and applications run in [user space](user-space.md) at ring 3. A [system call](system-call.md) lets an application request a kernel operation without giving the application ring 0 privileges.

## Example

When a Linux application opens a file, the processor switches from ring 3 to ring 0 and starts running the kernel's system-call handler. The kernel checks the request and returns the result to the application at ring 3.

## Privilege inside a guest

[Intel VT-x](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) separates [guest](guest.md) execution (VMX non-root operation) from [host](host.md) execution (VMX root operation). Each can use ring 0 and ring 3. A guest kernel at ring 0 has more privilege than its own applications, but it is still in guest operation. Moving from guest ring 3 to guest ring 0 is not a [VM exit](vm-exit.md).

[Back to Glossary](index.md)
