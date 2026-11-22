# Hardware-backed virtual machines

A [virtual machine (VM)](../../glossary/virtual-machine.md) gives an [agent](../../glossary/agent.md) a computer environment with its own operating-system [kernel](../../glossary/kernel.md). Its programs do not make their operating-system requests directly to the [host](../../glossary/host.md) kernel.

## Who handles the request?

When the [Lamp](../../practice/design/from-issue-to-patch.md) test runner makes a [system call](../../glossary/system-call.md) to open `total.c`, the [guest kernel](../../glossary/guest.md) handles it. The kernel looks for the path in the guest's filesystem. If the project is on a virtual disk or a shared directory, the guest can read it there. It cannot open arbitrary files on the host just because it can run ordinary Linux commands.

A [virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md) manages the VM and the devices the guest sees. For example, [Firecracker at revision `58cf1b2c`](https://github.com/firecracker-microvm/firecracker/blob/58cf1b2cdca407f2323d1b0b25ebb95dfe5b4bcb/docs/design.md) presents virtual disk and network devices to Linux guests. A [microVM](../../glossary/microvm.md) typically exposes fewer devices than a general-purpose VM. It still has a guest kernel. See [the VM, container, and microVM comparison](../../sandbox-isolation-boundaries.md#compare-a-vm-a-container-and-a-microvm) for the boundary and trade-offs side by side.

## What stays shared?

Two [containers](../../glossary/container.md) inside the same VM share its guest kernel. A VM per [pod](../../glossary/pod.md) is not the same as a VM per container. VMs on one host can still share physical hardware even though each runs its own guest kernel. Compare [which workloads share a guest kernel](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel) in the architecture survey.

## When to use it

Choose this boundary when an agent needs a full Linux [workspace](../../glossary/workspace.md) and the workload needs its own kernel. For example, run a native build and test suite without putting its processes directly on the host kernel.

## What the boundary does not cover

The guest can use files the host chooses to expose. A writable shared project directory lets the guest change the host files in that directory. Check what the guest can access through storage and through the network. If you reuse a [snapshot](../../glossary/snapshot.md), check whether it contains disk data, memory, or both before sharing it.

See [MicroVM](microvm.md) for the smaller virtual device set and what to check before reusing VM state. See the [architecture survey](../../agent-sandbox-architectures.md#hardware-backed-linux-environments) for VMMs and sandbox products that use them.
