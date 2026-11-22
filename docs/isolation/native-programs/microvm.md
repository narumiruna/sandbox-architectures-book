# MicroVM

A [microVM](../../glossary/microvm.md) is a [virtual machine (VM)](../../glossary/virtual-machine.md) designed to run with less overhead than a general-purpose VM. It typically offers fewer virtual devices, but it still runs its own operating-system [kernel](../../glossary/kernel.md). Use one when a job needs a separate kernel and the available devices are enough. “Micro” does not tell you how fast your job will start or how much memory it will use.

## Where the file request goes

1. The [Lamp](../../practice/design/from-issue-to-patch.md) test runner asks to open `total.c`. The Linux [guest kernel](../../glossary/guest.md) handles that [system call](../../glossary/system-call.md), not the [host](../../glossary/host.md) kernel.
2. The guest kernel looks up the path in its own filesystem. If the file is on a virtual disk, the guest kernel reads from that device as needed.
3. In [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#host-integration), the disk can be backed by a file on the host. Through that device, the guest sees the virtual disk, not the host's filesystem.

Firecracker, the [virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md), supplies virtual devices and [uses KVM to run the guest CPUs](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#internal-architecture). Its [device model](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#machine-model) includes virtual storage and networking but no graphical display device. Check the specific VMM rather than assuming all microVMs expose the same devices.

## Decide what to share and keep

- **Kernel:** Processes inside one microVM share its guest kernel. If jobs must not share a kernel, give each job its own microVM rather than putting several jobs in one.
- **State:** Compare a [cold boot](../../glossary/cold-boot.md) with a [snapshot](../../glossary/snapshot.md) restore if both are available. For example, [Firecracker v1.11.0 snapshots](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/snapshotting/snapshot-support.md#overview) save guest memory and emulated hardware state; the operator manages the backing disks separately. Check both for job data before reuse.
- **Access:** A separate kernel does not make a writable shared directory private from the guest or block outbound traffic. Set and [verify the access rules](../../practice/verification/verifying-access-rules.md) for files, network destinations, and credentials.

If the job does not need its own Linux kernel, [compare microVMs with gVisor](microvm-vs-gvisor.md).
