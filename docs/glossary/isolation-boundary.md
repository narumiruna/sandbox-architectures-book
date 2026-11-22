# Isolation boundary

An isolation boundary is the mechanism that separates running code from other code or resources. It can block direct access while still providing controlled ways to reach selected resources. The boundary is the mechanism; the rules for what may cross it are the policy. Naming the mechanism alone does not tell you what the code can reach.

## Example

A test job runs in a [sandbox](sandbox.md) built around a virtual machine. Without a shared workspace, the job cannot open project files on the host as if they were local. The service can choose to expose a copy of the source tree or a writable share. Both setups have a VM boundary, but only the writable share lets the job change the shared host files directly.

## What the mechanism separates

A [virtual machine](virtual-machine.md) separates a guest operating system from the host. An [operating-system process sandbox](operating-system-process-sandbox.md) restricts processes that still use the host operating system's kernel. A language runtime can instead restrict a script to certain operations and [host functions](host-function.md). See [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md) for the full comparison.

At each boundary, identify the protected resources, the component enforcing [policy](policy.md), and the paths it exposes. Then identify the [isolation unit](isolation-unit.md): two jobs in the same VM are both inside its boundary, so that VM boundary does not separate them from each other.

[Back to Glossary](../glossary.md)
