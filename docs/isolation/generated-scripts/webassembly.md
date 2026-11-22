# WebAssembly

[WebAssembly (Wasm)](../../glossary/webassembly.md) lets the host application run a module with checked memory access and a defined set of operations it can call outside the module. The module does not get a shell, filesystem, or network connection just because it runs.

## Where the boundary is

Suppose a generated program counts open issues. It can calculate the counts inside the sandbox. To get the issues, it calls a [host function](../../glossary/host-function.md) that the application supplied. The host checks which projects the caller may read and returns data to the program.

Two common designs place generated code behind this boundary:

1. **Run the workload as a Wasm module.** An application can compile the workload to Wasm and run it in a runtime such as [Wasmtime](https://docs.wasmtime.dev/security.html). A module can call the host operations that the application provides.
2. **Run a language engine as the Wasm module.** In [Pi at revision `9c465268`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md), QuickJS is compiled to Wasm. The model still writes JavaScript, which QuickJS interprets.

## When to use it

Choose this boundary when the workload or its language engine can run in Wasm and does not require ordinary Linux binaries. Check which operations the application supplies, rather than assuming [WASI](../../glossary/webassembly-system-interface.md) grants access to the host filesystem. Also check how the runtime limits memory and stops a program that runs too long.

See the [architecture survey](../../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells) for more ways to run tool scripts.
