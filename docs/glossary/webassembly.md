# WebAssembly (Wasm)

WebAssembly, abbreviated Wasm, is a portable format for executable code. A Wasm [runtime](runtime.md) can run the same code on different processors and operating systems if it supports the features the code needs. Wasm itself provides no filesystem, network connection, or shell. What the code can reach depends on what the [host](host.md) makes available.

## Example

A log service runs a Wasm module, a package of instructions and data, to count warnings. The host passes in the log text, and the module returns a count. The module does not need to open the log file itself, so the service does not grant it filesystem access.

## Memory and imports

When a runtime creates a runnable instance of a module, it connects the module's *imports*, the functions or other resources the module declares it needs from outside. The [WebAssembly Core Specification 1.0](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#imports) defines imports that can include functions or even memory. Wasm reads and writes its *linear memory*, a range of bytes the instance can use. An [access past that range](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#memory-instructions) stops execution with an error instead of reaching other memory in the host process.

The runtime's memory checks do not restrict the effects of a [host function](host-function.md). A function that reads files must enforce its own access rules, even when the caller cannot read files directly. The host can provide custom functions or standard interfaces such as the [WebAssembly System Interface (WASI)](webassembly-system-interface.md). To run a module elsewhere, check that the new environment supports the Wasm features and imports it needs.

## What is compiled to Wasm?

The workload can be a Wasm module, or the module can be a language engine that runs the workload. [Pi `codemode` at revision `9c465268`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) compiles QuickJS to Wasm and supplies tools to the JavaScript it runs. The engine is the Wasm module; the script is still JavaScript. The dependency name [`quickjs-wasi`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/package.json) does not tell you what access the script gets.

## When to use it

Consider Wasm for code that can run with selected host operations instead of a full operating system. An ordinary Linux [native binary](native-binary.md) cannot run directly as a Wasm module. See [WebAssembly in Foundations](../isolation/generated-scripts/webassembly.md) for a tool lookup example.

[Back to Glossary](index.md)
