# User space

User space is where applications and most services run, outside the operating system's [kernel](kernel.md). Programs in user space have less direct control over hardware and system resources than the kernel does. Running in user space is normal for applications and does not by itself make a program sandboxed.

## Example

An editor and a test runner can both run in user space on the same Linux machine. The editor can read personal files the user has access to. The sandbox lets the test runner read the project but not those personal files. The restriction comes from the sandbox, not from running in user space.

## How programs ask for kernel services

When a program needs to open a file or perform another kernel operation, it makes a [system call](system-call.md), often through a library. The [Linux system call introduction](https://man7.org/linux/man-pages/man2/intro.2.html) describes how the kernel handles the request and returns a result. A [user-space kernel](user-space-kernel.md) implements that interface as software outside the host kernel.

[Back to Glossary](../glossary.md)
