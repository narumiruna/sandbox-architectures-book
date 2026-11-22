# Kernel

A kernel is the core of an operating system. It manages resources such as CPU time, memory, files, and devices. Programs ask it to perform operations through [system calls](system-call.md), such as a request to open a file.

## Example

Two test sandboxes on the same Linux machine can see different project directories but still ask the same Linux kernel to open their files. If each sandbox instead runs inside its own [virtual machine](virtual-machine.md), each test program asks its own VM's kernel to open files on the storage available to that VM.

## Which kernel handles the request?

A regular [operating-system process sandbox](operating-system-process-sandbox.md) uses the *host kernel*: the kernel of the underlying operating system. The kernel applies controls such as [namespaces](namespace.md) and [seccomp](seccomp.md) to those processes. A VM runs a *guest kernel* that manages the resources presented to the VM. A [user-space kernel](user-space-kernel.md) takes a third approach: it implements the workload's kernel interface as software outside the host kernel. See [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md) for the differences.

[Back to Glossary](../glossary.md)
