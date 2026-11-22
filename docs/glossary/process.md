# Process

A process is a running instance of a program. A [native binary](native-binary.md) is a file a system can execute; a process is what runs when the system starts that program. Two runs of the same program can have different memory, open files, and permissions.

## Example

When an agent starts Lamp's test runner, the operating system starts a process that can ask to open `total.c`. The process makes a [system call](system-call.md) to request that operation from the [kernel](kernel.md). Another invocation of the same runner can see a different set of files if it runs with a different sandbox configuration.

## When it matters

In an [operating-system process sandbox](operating-system-process-sandbox.md), the host kernel enforces restrictions on the running process. A test runner can start other processes, called child processes. Check that restrictions also apply to those processes and that they inherit only the data and open files they need. By contrast, a process inside a [virtual machine](virtual-machine.md) uses the VM's own kernel.

See [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md#follow-a-request-to-open-a-file) for the path a file request takes.

[Back to Glossary](index.md)
