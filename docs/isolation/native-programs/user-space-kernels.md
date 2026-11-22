# User-space kernels

A [user-space kernel](../../glossary/user-space-kernel.md) lets an [agent](../../glossary/agent.md) run Linux programs without booting a separate Linux [guest](../../glossary/guest.md). It implements the Linux interface that those programs expect, so their requests do not go straight to the [host](../../glossary/host.md) [kernel](../../glossary/kernel.md).

## Who handles the request?

When the [Lamp](../../practice/design/from-issue-to-patch.md) test runner makes a [system call](../../glossary/system-call.md) to open `total.c` in [gVisor](https://gvisor.dev/docs/architecture_guide/intro/), gVisor's **Sentry** handles the request. The Sentry resolves the path in the runner's view of the filesystem. gVisor can make its own limited host requests to get data; it does not simply forward the workload's system call unchanged.

## What stays shared?

Programs in the same gVisor sandbox share the Sentry. gVisor still relies on the host kernel for underlying resources. A [VM](../../glossary/virtual-machine.md), by contrast, boots a guest kernel. In a [process sandbox](operating-system-process-sandboxes.md), the program makes its own system calls to the host kernel.

## When to use it

Choose this boundary when you need to run Linux [containers](../../glossary/container.md) but want a layer between the workload and the host kernel. Because the Linux interface is reimplemented, a program can depend on behavior that is [not supported or works differently in gVisor](https://gvisor.dev/docs/user_guide/compatibility/). Test the actual install, build, and test steps, not just whether the commands start.

## What the boundary does not cover

The Sentry serves the filesystem view it is given. It does not decide which Lamp data the agent should be allowed to read. Verify that the [runtime](../../glossary/runtime.md) exposes only the intended [workspace](../../glossary/workspace.md) and network access.

See [gVisor](gvisor.md) for how its runtime exposes files and what changes when it uses KVM.
