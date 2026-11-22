# Engine isolates

An [engine isolate](../../glossary/engine-isolate.md) keeps a script's objects and execution state separate within a language engine such as [V8](https://github.com/v8/v8/blob/13.8.258/include/v8-isolate.h#L277-L285). The platform that embeds the engine decides which APIs the code can use.

## Who handles the request?

When a script asks for the title of [`LAMP-17`](../../practice/design/from-issue-to-patch.md), the engine runs the script and the platform routes the request through the named connection to the issue service. The issue service checks [authorization](../../glossary/authorization.md) for the issue before returning its title.

[Cloudflare Dynamic Workers](https://blog.cloudflare.com/dynamic-workers/) provides this kind of execution environment for JavaScript. In Cloudflare's documented example, a caller can set `globalOutbound: null` to block ordinary outbound requests and still supply a specific **binding**, a named connection to another service.

## What stays shared?

Isolates can share an operating-system [process](../../glossary/process.md) even though the engine separates their script state. The platform can also connect multiple isolates to the same service. An isolate is not a separate process or a [VM](../../glossary/virtual-machine.md).

## When to use it

Choose this boundary when a script needs the language engine's features and a few platform APIs, but not a shell or native packages.

## What the boundary does not cover

A binding that can fetch arbitrary URLs would grant broad access even if the script cannot make direct network requests. Review the worker's bindings and default network access together. Also check which scripts share a process and what other controls the platform applies around the engine.
