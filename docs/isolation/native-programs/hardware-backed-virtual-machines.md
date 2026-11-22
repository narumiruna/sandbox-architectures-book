# Hardware-backed virtual machines

A [virtual machine (VM)](../../glossary/virtual-machine.md) gives an agent a computer environment with its own operating-system [kernel](../../glossary/kernel.md). An agent can run a Linux build inside the VM without running the build processes directly on the host kernel.

## Where the boundary is

When a build reads a project file, the request first goes to the **guest kernel**, the operating-system kernel inside the VM. The guest reads from a disk or shared directory that the host chose to expose. A file on the host is not visible just because the guest can run ordinary Linux commands.

A [virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md) manages the VM and the devices the guest sees. For example, [Firecracker at revision `58cf1b2c`](https://github.com/firecracker-microvm/firecracker/blob/58cf1b2cdca407f2323d1b0b25ebb95dfe5b4bcb/docs/design.md) presents virtual disk and network devices to Linux guests. A [microVM](../../glossary/microvm.md) typically exposes fewer devices than a general-purpose VM. It still has a guest kernel.

## When to use it

Choose this boundary when an agent needs a full Linux workspace and the workload needs its own kernel. Check three things:

1. **Which workloads share a VM?** Two containers inside the same VM share its kernel. A VM per pod is not the same as a VM per container.
2. **What does the host expose?** A writable shared project directory lets the guest change host files in that directory. Review network access separately from disk access.
3. **What survives the run?** Measure startup and restore separately. If you reuse a [snapshot](../../glossary/snapshot.md), check whether it contains disk data, memory, or both before sharing it.

See the [architecture survey](../../agent-sandbox-architectures.md#hardware-backed-linux-environments) for VMMs and sandbox products that use them.
