# Control group (cgroup)

A control group, or cgroup, groups Linux processes so the operating system can measure or limit the resources they use, such as CPU time and memory. A cgroup does not decide which files the processes can open or which network destinations they can reach.

## Example

A build sandbox places a compiler and its worker processes in one cgroup. The service can measure memory use for the whole job and set a limit so the job cannot use all the machine's memory.

## How Linux manages resources for a group

In [Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), groups form a tree. *Controllers* are the parts of the [kernel](kernel.md) that manage particular resources for those groups. For example, the CPU controller can limit the group's CPU time, and the memory controller can track the group's memory use and enforce a memory limit.

Use [namespaces](namespace.md) for separate views of resources and a separate [policy](policy.md) to control file and network access. Those controls do different jobs from resource accounting and limits.

[Back to Glossary](index.md)
