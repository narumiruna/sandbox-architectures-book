# WebAssembly

[WebAssembly (Wasm)](../../glossary/webassembly.md) lets a [host](../../glossary/host.md) application run a module with checked memory access and a defined set of operations it can call outside the module. The module does not get a shell, filesystem, or network connection just because it runs.

## Who handles the request?

When a program asks for the title of [`LAMP-17`](../../practice/design/from-issue-to-patch.md), the Wasm [runtime](../../glossary/runtime.md) lets the module call the [host function](../../glossary/host-function.md) that the application provided for issue lookup. The host function checks [authorization](../../glossary/authorization.md) for the issue before returning its title. Sorting the titles can run inside the module.

Two common designs place generated code behind this boundary:

1. **Run the workload as a Wasm module.** An application can compile the workload to Wasm and run it in a runtime such as [Wasmtime](https://docs.wasmtime.dev/security.html). A module can call the host operations that the application provides.
2. **Run a language engine as the Wasm module.** In [Pi at revision `9c465268`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md), QuickJS is compiled to Wasm. The model still writes JavaScript, which QuickJS interprets.

## What stays shared?

Modules can run in the same host [process](../../glossary/process.md) without having access to each other's memory by default. The host can explicitly supply the same resource, such as an issue lookup service, to more than one module.

## When to use it

Choose this boundary when the workload or its language engine can run in Wasm and does not require ordinary Linux [binaries](../../glossary/native-binary.md).

## What the boundary does not cover

Memory checks do not limit what the host function does on behalf of the module. Check which operations the application supplies, rather than assuming the [WebAssembly System Interface (WASI)](../../glossary/webassembly-system-interface.md) grants access to the host filesystem. Also check how the runtime limits memory and stops a program that runs too long.

See the [architecture survey](../../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells) for more ways to run tool scripts.
