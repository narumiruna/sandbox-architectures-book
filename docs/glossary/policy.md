# Policy

A policy is a set of rules about which actions running code may take and which resources it may use. A rule only has an effect if a trusted component applies it. An instruction to a model is not an access restriction by itself.

## Example

A test [sandbox](sandbox.md) may read project files, write temporary output, and fetch dependencies from an approved package registry. The operating system enforces which files are read-only and which can be written. A network proxy checks each destination against an [allowlist](allowlist.md), and the setup blocks direct network access so the test cannot simply go around the proxy.

## Match each rule to an enforcer

The [control plane](control-plane.md) can select the policy when it creates the sandbox. The runtime, operating system, proxy, or [tool](tool.md) handler enforces the part it can observe. For example, the [Linux kernel documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html) explains that [seccomp](seccomp.md) can filter requests to the kernel, but its filters cannot read a filename when the request gives only the filename's location in memory. For direct file access, use a filesystem control to enforce a rule about file paths.

Check what should succeed and what should fail at each [isolation boundary](isolation-boundary.md). If the same resource is reachable through both a mount and a tool, check both paths. A denial on one path is not a denial on the other.

[Back to Glossary](../glossary.md)
