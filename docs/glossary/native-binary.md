# Native binary

A native binary is a program compiled into instructions for a particular type of processor and operating system interface. It needs a compatible environment. A Linux native binary is not a [WebAssembly](webassembly.md) module and cannot run directly as one.

## Example

A code review sandbox runs an existing linter built for 64-bit Arm Linux. A Linux [virtual machine](virtual-machine.md) with that processor architecture and the required libraries can run it. To run the linter directly in a Wasm runtime, the service would supply a Wasm build instead of the Linux executable.

## What compatibility depends on

The executable format tells the operating system how to load the program. For example, a Linux [ELF executable](https://man7.org/linux/man-pages/man5/elf.5.html) records its target processor architecture. If the program uses shared libraries, the environment also needs a compatible [loader and libraries](https://man7.org/linux/man-pages/man8/ld.so.8.html). The program's [system calls](system-call.md) must be supported by the kernel interface it runs against. A matching processor alone is not enough.

[Back to Glossary](index.md)
