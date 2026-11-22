# Isolation boundary

An isolation boundary is the mechanism that separates running code from other code or resources. It can block direct access while still providing controlled ways to reach selected resources. The boundary is the mechanism; the [policy](policy.md) specifies what may cross it. Naming the mechanism alone does not tell you what the code can reach.

## Example

Lamp's test job runs in a [sandbox](sandbox.md) built around a [virtual machine (VM)](virtual-machine.md). The service can give the test runner a copy of `total.c` or expose the project through a writable share. Both setups have a VM boundary, but only the writable share lets the test job change the original file directly.

## What the mechanism separates

A VM separates a guest operating system from the [host](host.md). An [operating-system process sandbox](operating-system-process-sandbox.md) restricts [processes](process.md) that still use the host [kernel](kernel.md). A language [runtime](runtime.md) can instead restrict a script to certain operations and [host functions](host-function.md). See [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md) for the full comparison.

## When it matters

When choosing an environment for code you do not trust, identify the resources it must protect, the component enforcing policy, and the paths it exposes. Then identify the [isolation unit](isolation-unit.md): two jobs in the same VM are both inside its boundary, so that VM boundary does not separate them from each other.

[Back to Glossary](../glossary.md)
