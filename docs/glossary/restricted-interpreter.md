# Restricted interpreter

A restricted interpreter runs code using only the language features and built-in operations it implements. Code can reach outside the interpreter only through operations the [host](host.md) provides. A small language does not guarantee small permissions: one host operation can still grant broad access.

## Example

A build service lets a script count failed tests using lists, loops, and a [tool](tool.md) that reads results for an approved build. The script cannot open arbitrary files or start commands. The service still checks that the caller may read the requested build before the tool returns any results.

## Supported language and libraries

An interpreter evaluates the script according to its own rules. A restricted interpreter can omit syntax, built-in operations, or library support. Code can look like JavaScript without supporting the same packages or operations as a general JavaScript environment. This approach does not require [WebAssembly](webassembly.md) or an [engine isolate](engine-isolate.md).

For example, [OpenCode Code Mode at revision `5310e422`](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md) uses Psychoscript to interpret a JavaScript-like language. At that revision it does not load packages or give scripts direct filesystem, network, or process access. The host supplies tools for work outside the interpreter.

## Limits beyond the language

A supported loop can still run too long, and an approved tool call can still return more data than expected. Limit execution time, memory, and tool use separately. Apply [least privilege](least-privilege.md) to each tool: a test-results reader should not also offer a way to run arbitrary commands.

[Back to Glossary](../glossary.md)
