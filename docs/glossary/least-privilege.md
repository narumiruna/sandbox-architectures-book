# Least privilege

Least privilege means giving code only the permissions it needs for its task. Limit what it can do, what it can act on, and how long it needs access. The test is what the code can actually reach, including through tools, not just what its settings say.

## Example

A dependency report needs to read a project's package manifest and look up version information. Its [sandbox](sandbox.md) exposes a read-only copy of the manifest and a version lookup [tool](tool.md) for an approved registry. The job does not need workspace write access, an unrestricted network connection, or a registry token of its own.

## Narrow each grant

First identify the operations the [workload](workload.md) needs. Scope file access to the necessary files, separate reading from writing, and prefer a specific tool operation over a general interface when that operation is enough. If a service must authenticate a request, it can use [credential injection](credential-injection.md) on approved requests rather than handing the code a reusable secret. End temporary access when the job finishes.

Check each allowed path on its own. A read-only [mount](mount.md) prevents writes through that mount, but it does not stop a separate tool from writing to the same files. The tool handler must enforce its own limits. Least privilege reduces what the workload can affect; it does not prevent harm from actions that the workload is allowed to take.

[Back to Glossary](../glossary.md)
