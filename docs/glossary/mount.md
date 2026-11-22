# Mount

To mount a filesystem or directory is to make its files visible at a path. A *bind mount* makes an existing file or directory visible at another path without copying it. If a sandbox can write through a bind mount, it can change the original files.

## Example

A code review sandbox sees the host's project directory at `/workspace`. The service gives the sandbox a read-only mount of that directory. The review program can inspect the project but cannot change it through `/workspace`. It writes its report to a separate output directory.

## Which files a workload sees

A [mount namespace](namespace.md) can give a process group its own view of what is mounted. The Linux [`mount(2)` documentation](https://man7.org/linux/man-pages/man2/mount.2.html) distinguishes the mount's settings from the underlying filesystem. A read-only bind mount blocks writes through that mount, but it does not make the underlying files read-only through other mounts. It also does not hide file contents. Only mount the files that the [workload](workload.md) needs to see.

[Back to Glossary](../glossary.md)
