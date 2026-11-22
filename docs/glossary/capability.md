# Capability

In this book, a capability is a resource or operation that code can use because the system running it has granted access. To understand what was granted, ask both what the code can do and what it can do it to. A narrow grant does not cancel broader access that the code gets another way.

## Example

A reporting script runs in a [sandbox](sandbox.md) with one [tool](tool.md) that returns the title of an issue in a particular project. The script gets the ability to read those titles, not to edit issues or make arbitrary network requests. The service that handles the call uses its own [credential](credential.md) without giving it to the script.

## What a grant covers

A [host function](host-function.md) can grant an operation such as issue lookup. A read-only [mount](mount.md) can grant access to files without granting the ability to change them through that mount. In each case a component outside the workload enforces the limit: the tool handler checks the requested issue, or the operating system enforces read-only access.

Judge a capability by its effect, not its name. A tool called “read issue” is only project-scoped if the handler checks the requested project. A script with general network access and an API token may be able to act without that tool, so evaluate both direct access and access through tools when applying [least privilege](least-privilege.md).

[Back to Glossary](index.md)
