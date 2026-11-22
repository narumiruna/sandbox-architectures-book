# Engine isolate

An engine isolate is a separate execution environment inside a language engine, the software that runs code in a language such as JavaScript. An isolate has its own state, including the objects its scripts create. Isolates can share one operating-system process, so an isolate is not a separate process or a [virtual machine](virtual-machine.md).

## Example

An issue tracker runs scripts from two teams in separate isolates. A script can keep a list of issue titles in memory without the other script seeing it. To get the titles, each script calls a [host function](host-function.md) that checks which project the script is allowed to read.

## Engine state and host access

The [V8 13.8.258 Isolate API](https://github.com/v8/v8/blob/13.8.258/include/v8-isolate.h#L277-L285) specifies separate state: V8 objects from one isolate must not be used in another. The engine manages that separation. The [host](host.md), the application that embeds the engine, decides which operations scripts can call. [Cloudflare's Dynamic Workers architecture](https://blog.cloudflare.com/dynamic-workers/) illustrates this distinction: a caller can give the script named access to selected services and block direct outbound requests.

An isolate does not limit what a host function does on the script's behalf. Check each exposed operation against the script's permissions, and check how the platform limits CPU and memory use. If a task needs to run native programs, use a separate environment that supports them, such as an [operating-system process sandbox](operating-system-process-sandbox.md).

[Back to Glossary](index.md)
