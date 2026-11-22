# WebAssembly System Interface (WASI)

The [WebAssembly System Interface (WASI)](https://wasi.dev/) is a family of standard interfaces that a host can offer to [WebAssembly](webassembly.md) programs for tasks such as reading files or checking the time. WASI describes how to ask for these services. It is not an operating system, and support for an interface does not grant access to every resource it can describe.

## Example

A sandbox gives a report generator read-only access to a directory of test results through WASI. The report generator can read those results without receiving the host's entire filesystem. It cannot write to that directory through the read-only access it was given.

## Interfaces and permissions

A Wasm program declares the interfaces it expects as imports. These are requests for functions or resources that must be supplied from outside the program. The host chooses what access to grant through those interfaces. In WASI 0.2.0, for example, the [filesystem preopens interface](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/filesystem/preopens.wit) lists directories the program has been given access to at startup. The [filesystem types](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/filesystem/types.wit) require paths to stay within the directory identified by a *handle*, a reference used to make filesystem requests. Access flags can prevent changes through that handle.

Review the actual grants, not just the interface names. A program can also receive custom [host functions](host-function.md) that provide access outside WASI. Those functions need their own permission checks.

## Version and operating-system compatibility

[WASI Preview 1](https://wasi.dev/releases/wasi-p1) uses core Wasm module imports under the name `wasi_snapshot_preview1`. [WASI 0.2 (Preview 2)](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/README.md) uses the WebAssembly Component Model, which connects Wasm components through interfaces described in WIT, a language for naming functions and their data types. Check the version and interfaces the program expects against what the [runtime](runtime.md) and host provide. WASI does not provide a Linux kernel or make an ordinary Linux [native binary](native-binary.md) runnable as Wasm.

[Back to Glossary](index.md)
