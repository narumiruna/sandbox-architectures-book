# Restricted interpreters

A [restricted interpreter](../../glossary/restricted-interpreter.md) runs only the language features and built-in operations that it implements. The host supplies any extra operations the script can call, such as a tool that looks up an issue. A familiar language name does not mean the usual libraries or system APIs are available.

## Where the boundary is

Suppose a script calls an issue lookup tool and counts the results. Loops and arithmetic run inside the interpreter. The lookup itself runs in a host tool, which must check access to the requested project. The script does not need an issue tracker library or direct network access.

[OpenCode at revision `5310e422`](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md) uses Psychoscript for a JavaScript subset. [Pydantic AI Code Mode](https://pydantic.dev/docs/ai/harness/code-mode/) uses [Monty, shown at revision `5f4a3dfc`](https://github.com/pydantic/monty/blob/5f4a3dfc493538bb9dc319974393391ba9e7cf14/README.md), for a Python subset. Both can let generated code call tools without providing a full language environment.

## When to use it

Choose this boundary when the script mostly combines tool calls and processes results. Check which language features, built-ins, and imports the interpreter supports, and how it stops long-running scripts. Test with the kind of code the model is likely to generate; short, valid Python or JavaScript may still use a feature outside the supported subset.

Review host tools separately. An interpreter without file access can still change host files if you give it an unrestricted write tool.
