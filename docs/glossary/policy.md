# Policy

A policy is a set of rules about which actions running code may take and which resources it may use. A rule only has an effect if a trusted component applies it. An instruction to a model is not an access restriction by itself.

## Example

Lamp's test [sandbox](sandbox.md) may read `total.c` and write temporary output, but may not open the [host](host.md)'s SSH keys. In a [process sandbox](operating-system-process-sandbox.md), the sandbox setup makes the project files read-only and a temporary directory writable. The host [kernel](kernel.md) checks each file request against that setup; the keys are not in the runner's view.

## Match each rule to an enforcer

The [control plane](control-plane.md) can select the policy when it creates the sandbox. The [runtime](runtime.md), operating system, proxy, or [tool](tool.md) handler enforces the part it can observe. For example, the [Linux kernel documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html) explains that [seccomp](seccomp.md) can filter requests to the kernel, but its filters cannot read a filename when the request gives only the filename's location in memory. For direct file access, use a filesystem control to enforce a rule about file paths.

## When it matters

When you configure or test a sandbox, check what should succeed and what should fail at each [isolation boundary](isolation-boundary.md). If the same resource is reachable through both a [mount](mount.md) and a tool, check both paths. A denial on one path is not a denial on the other. See [Follow a request to open a file](../sandbox-isolation-boundaries.md#follow-a-request-to-open-a-file) for the two parts of the file rule.

[Back to Glossary](index.md)
