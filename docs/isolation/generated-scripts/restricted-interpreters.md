# Restricted interpreters

A [restricted interpreter](../../glossary/restricted-interpreter.md) runs only the language features and built-in operations that it implements. The [host](../../glossary/host.md) supplies any extra operations the script can call. A familiar language name does not mean the usual libraries or system APIs are available.

## Who handles the request?

When a script asks for the title of [`LAMP-17`](../../practice/design/from-issue-to-patch.md), the interpreter runs the script but delegates the lookup to a host [tool](../../glossary/tool.md). The tool checks [authorization](../../glossary/authorization.md) for the issue before returning its title. Loops and sorting run inside the interpreter. The script does not need an issue tracker library or direct network access.

[OpenCode at revision `5310e422`](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md) uses Psychoscript for a JavaScript subset. [Pydantic AI Code Mode](https://pydantic.dev/docs/ai/harness/code-mode/) uses [Monty, shown at revision `5f4a3dfc`](https://github.com/pydantic/monty/blob/5f4a3dfc493538bb9dc319974393391ba9e7cf14/README.md), for a Python subset. Both can let generated code call tools without providing a full language environment.

## What stays shared?

An interpreter can run in the host application's [process](../../glossary/process.md). Limiting the language does not itself separate operating systems or give each script a process. Different scripts can also use the same host tools.

## When to use it

Choose this boundary when the script mostly combines tool calls and processes results. Test with the kind of code the model is likely to generate: short, valid Python or JavaScript may still use a feature or library outside the supported subset.

## What the boundary does not cover

A script with no direct file access can still change host files if it can call an unrestricted write tool. Review the host tools separately. Also check how the interpreter stops long-running scripts, since even a supported loop can run for too long.
