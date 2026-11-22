# Engine isolates

An [engine isolate](../../glossary/engine-isolate.md) keeps a script's objects and execution state separate within a language engine such as V8. The script runs in that engine, not in its own operating system. The platform that embeds the engine decides which APIs the code can use.

## Where the boundary is

Suppose a script counts open issues using a single issue lookup service. The platform can give the script a named connection to that service without giving it a general network connection.

[Cloudflare Dynamic Workers](https://blog.cloudflare.com/dynamic-workers/) provides this kind of execution environment for JavaScript. In Cloudflare's documented example, a caller can set `globalOutbound: null` to block ordinary outbound requests and still supply a specific **binding**, a named connection to another service. The issue service must still check which projects a request may read.

## When to use it

Choose this boundary when a script needs the language engine's features and a few platform APIs, but not a shell or native packages. Review the worker's bindings and default network access together. A binding that can fetch arbitrary URLs would grant broad access even if the script cannot make direct network requests.

An isolate is not an operating-system process or a VM. When evaluating a service, check which scripts share a process and what other controls the platform applies around the engine.
