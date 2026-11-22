# Operating-system process sandbox

An operating-system process sandbox runs programs directly on the [host kernel](kernel.md) and uses that operating system's controls to limit what the programs can access or do. It does not start a separate [guest](guest.md) kernel.

## Example

A local code review sandbox runs the host's search tools with read access to the project and write access to a temporary output directory. The tools do not need a separate operating system, but they and their child processes should remain subject to the same restrictions.

## Controls that work together

On Linux, [namespaces](namespace.md) can restrict the view of mounted filesystems or network interfaces. Path-based rules, such as those described in the [Linux 6.12 Landlock guide](https://docs.kernel.org/6.12/userspace-api/landlock.html#layers-of-file-path-access-rights), can restrict actions on file hierarchies. [Seccomp](seccomp.md) can filter system calls, while [cgroups](control-group.md) measure and limit resource use. None of these controls substitutes for the others. Check what the policy permits and that it covers child processes as well as the program the sandbox starts.

[Back to Glossary](../glossary.md)
