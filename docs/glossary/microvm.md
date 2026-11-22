# MicroVM

A microVM is a [virtual machine](virtual-machine.md) designed to reduce the work and resources needed to start and run it, usually by offering fewer virtual devices than a general-purpose VM. It still runs its own operating-system [kernel](kernel.md). The name does not promise a particular boot time or security level.

## Example

A test service gives each job a Linux microVM with a virtual disk and a network connection but no graphical display device. The job can run its usual command-line tools. A workload that needs a device the microVM does not expose would need a different configuration or another environment.

## What the smaller device set changes

A [virtual machine monitor](virtual-machine-monitor.md) for microVMs can omit devices its target workloads do not need. For example, [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/README.md) omits unnecessary devices and guest-facing features to reduce overhead and the code a guest can reach. A smaller device model also means less flexibility for workloads that expect other hardware.

The [isolation unit](isolation-unit.md) depends on the service: a microVM can contain one job or several workloads. Workloads in the same microVM share a guest kernel. Also check which host files and network services the sandbox exposes; a smaller VM does not decide what access is allowed.

[Back to Glossary](../glossary.md)
