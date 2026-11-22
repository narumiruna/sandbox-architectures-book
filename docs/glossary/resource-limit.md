# Resource limit

A resource limit caps how much a job may use, such as memory, disk space, CPU time, or concurrent workers. It does not decide which files or services the job can access.

For example, a disk limit can stop an agent's build from filling storage. It does not stop the build from reading data in a directory that was exposed by mistake. Use [policy](policy.md) to control access separately.

See [Resource limits](../practice/operations/resource-limits.md).
