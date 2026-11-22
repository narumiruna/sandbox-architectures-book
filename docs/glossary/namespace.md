# Namespace

A namespace gives a group of Linux processes its own view of a system resource, such as process IDs, mounted filesystems, or network interfaces. Giving processes separate namespaces does not give them separate [kernels](kernel.md).

## Example

A test sandbox uses a mount namespace to show the test runner a project directory at `/workspace` without showing the host's home directories. A separate [process ID namespace](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html) lets the test runner see the job's processes but not unrelated processes on the host.

## A separate view is not a permission rule

Linux has [different namespace types](https://man7.org/linux/man-pages/man7/namespaces.7.html) for different resources. Changing what is mounted does not give the workload its own network view. A file shared through a writable [mount](mount.md) can still be changed if permissions allow it.

Namespaces shape what processes see. Path-based access controls decide what processes may do to files, [seccomp](seccomp.md) filters system calls, and [control groups](control-group.md) account for or limit resource use.

[Back to Glossary](../glossary.md)
