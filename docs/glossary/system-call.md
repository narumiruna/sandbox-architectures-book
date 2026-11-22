# System call (syscall)

A system call, or syscall, is a request from a program to its operating system's [kernel](kernel.md). Opening a file, starting a process, and sending data through a network socket are examples of operations programs request this way.

## Example

A compiler in a build sandbox asks to open `/workspace/main.c`. In a shared-kernel sandbox, the host kernel resolves that path using the compiler's view of mounted filesystems and checks whether the compiler may open the file. If access is denied, the request fails.

## How the request is handled

Programs often call a library function that makes the actual system call, as the [Linux system call introduction](https://man7.org/linux/man-pages/man2/intro.2.html) explains. In a shared-kernel sandbox, the host kernel handles the call and can filter it with [seccomp](seccomp.md). In a [virtual machine](virtual-machine.md), the guest kernel handles its programs' calls. A [user-space kernel](user-space-kernel.md) can implement the same interface without forwarding each request directly to the host kernel.

[Back to Glossary](index.md)
