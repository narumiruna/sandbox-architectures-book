# Seccomp

Seccomp is a Linux feature that can filter [system calls](system-call.md), the requests a program makes to the kernel. It can block particular types of requests, but it does not by itself enforce file access rules based on a pathname.

## Example

A document conversion sandbox can use seccomp to block requests to create network sockets. Blocking creation alone does not restrict the use of sockets the program already has. A separate filesystem policy limits where the converter can read input files and write results.

## What the filter can inspect

The [Linux seccomp filter documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html) explains that a filter can inspect the system call number and the raw argument values. It can allow the call or, for example, make it fail without running it. A file path passed to a call such as `openat` is text stored in the program's memory. The filter sees the address of the text, not the text itself.

Use [mounts](mount.md) to control what files are visible and file access rules to control operations on them. A [control group](control-group.md) handles a different problem: measuring or limiting resource use.

[Back to Glossary](index.md)
