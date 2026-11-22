# User-space kernels

A [user-space kernel](../../glossary/user-space-kernel.md) lets an agent run Linux programs without booting a separate Linux guest. It implements the Linux interface that those programs expect, so their requests do not go straight to the host kernel.

## Where the boundary is

A [system call](../../glossary/system-call.md) is a program's request to the operating system, such as opening a file. When a build tool in [gVisor](https://gvisor.dev/docs/architecture_guide/intro/) asks to open a file, the **Sentry**, gVisor's user-space kernel, handles the workload's request. To get data from outside the sandbox, gVisor can use its own limited host operations. It does not simply forward each workload system call unchanged.

This differs from both a [VM](hardware-backed-virtual-machines.md), which provides a guest kernel, and a [process sandbox](operating-system-process-sandboxes.md), which puts restrictions around an application that still makes its own system calls to the host kernel.

## When to use it

Choose this boundary when you need to run Linux containers but want a layer between the workload and the host kernel. Because the Linux interface is reimplemented, a program can depend on behavior that is [not supported or works differently in gVisor](https://gvisor.dev/docs/user_guide/compatibility/).

Test the actual package install, build, and test steps. A command that starts successfully may still depend on an unsupported operation later. Also verify that the runtime exposes only the intended workspace and network access. The Sentry does not decide which project data the agent should be allowed to read.
