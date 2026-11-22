# Host

The host is the system outside a [sandbox](sandbox.md) that provides resources to it. For a [virtual machine](virtual-machine.md), this usually means the machine or operating system that runs the VM. For a language sandbox, it can mean the application that runs the script engine. *Host* names a role relative to a particular boundary.

## Example

A build service runs a Linux [guest](guest.md) on a server. The host supplies CPU time and memory and backs the VM's disk with a file. The team chooses to expose the project directory through a read-only [mount](mount.md) so the build can read the source without changing the host copy.

## Resources and access

The host side sets up the boundary and provides ways to cross it. A VM may receive a virtual disk and a network connection. A script sandbox may receive a [host function](host-function.md) that reads a single project file. These choices affect what the workload can do; the presence of a boundary does not make a broad resource grant safe.

The host is not necessarily the [control plane](control-plane.md). A control plane can decide where to place a sandbox while a different machine runs it. When a design says “host,” identify the boundary and the component that actually supplies the resource.

[Back to Glossary](../glossary.md)
