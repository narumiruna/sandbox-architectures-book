# Host function

A host function is an operation implemented outside a language sandbox and made callable by the code inside it. The application that runs the sandbox decides which functions to expose. The function runs with the permissions of the component that implements it, not just the permissions of the calling script.

## Example

A script in a [sandbox](sandbox.md) needs a project's version number. The application exposes a host function that reads the version from that project's manifest and returns only the version string. The script can get the value without receiving general access to the project's files.

## What crosses the boundary

The language runtime supplies a way to call into the surrounding application. For example, a [WebAssembly](webassembly.md) module can call a function that the application supplies as an *import*, an operation provided from outside the module. The [Wasmtime security documentation](https://docs.wasmtime.dev/security.html#webassembly-core) explains how explicitly supplied imports let the application control what a module can do outside its own memory.

A [tool](tool.md) is an operation offered to an agent or script; a host function is one way to make that operation callable from a language sandbox. Some host functions instead supply basic services, such as a clock. In either case, the handler must enforce the relevant [policy](policy.md) on its inputs, effects, and returned data. The script's own restrictions do not do that job for it.

[Back to Glossary](../glossary.md)
