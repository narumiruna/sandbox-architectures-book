# Runtime

A runtime is software that runs code or sets up the environment that runs it. The word alone does not tell you what kind of code can run or what keeps it separate from other programs.

## Example

An agent service runs a report generator compiled to [WebAssembly](webassembly.md) in a sandbox with access to test results. To run a new test, the service starts a build container through a [container runtime](container-runtime.md). The Wasm runtime executes the report generator; the container runtime prepares an environment for the native test program.

## What the runtime runs or prepares

A language runtime can run scripts with a language engine or a [restricted interpreter](restricted-interpreter.md). A Wasm runtime loads and runs modules, which are packages of Wasm instructions and data. When the runtime creates a runnable instance of a module, the application can supply selected [host functions](host-function.md). A container runtime instead sets up the filesystem and other resources for a process. For example, the [OCI Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/blob/v1.2.1/runtime.md#lifecycle) describes creating a container environment from a configuration before starting the program.

## Management is not isolation

A [control plane](control-plane.md) can decide where and when to start a sandbox, while the runtime runs the code or prepares its environment. One product can do both. To identify the [isolation boundary](isolation-boundary.md), ask what enforces separation and what host resources the workload can use. For example, a container runtime can start processes that share the host kernel or place them inside a VM with a separate kernel.

[Back to Glossary](index.md)
