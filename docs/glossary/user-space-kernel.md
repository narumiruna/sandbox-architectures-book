# User-space kernel

A user-space kernel is software that handles a workload's operating-system requests outside the [host kernel](kernel.md). It provides the interface that the programs expect without needing to boot a separate guest kernel. It still relies on the host kernel for resources, and it may not support every operation the programs expect.

## Example

In a build sandbox that uses gVisor, a test program asks for its process ID. As the [gVisor architecture guide](https://gvisor.dev/docs/architecture_guide/intro/) explains, gVisor's Sentry answers from its own process records instead of asking the host kernel for the sandboxed program's process ID.

## Handling calls instead of filtering them

The Sentry implements Linux [system calls](system-call.md) rather than simply allowing or denying calls to the host. It can make its own, more limited requests to the host kernel; those requests need not match the workload's calls one for one. This differs from a shared-kernel [process sandbox](operating-system-process-sandbox.md), where the host kernel implements the calls the process is allowed to make. Test the interfaces and performance the workload needs rather than assuming it will behave exactly as it does on Linux directly.

[Back to Glossary](../glossary.md)
