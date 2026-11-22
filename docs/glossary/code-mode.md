# Code Mode

Code Mode is a pattern in which a model writes a program that calls tools and combines their results. The term describes how the model uses tools, not what keeps the program separate from the rest of the system. Even if the program runs in a sandbox, the tool handlers and the rest of the agent may run outside it.

## Example

An [agent](agent.md) needs a list of milestones with open issues. Instead of asking the model for each issue lookup separately, it runs one generated script in a [sandbox](sandbox.md). The script calls the issue lookup tool for each milestone, counts the results, and returns a short summary. The agent can use that summary in its next decision.

## Running the generated program

The application chooses the tools that the script can call and which [runtime](runtime.md) runs it. For example, [Pi `codemode` at the revision covered by the book](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) runs JavaScript in QuickJS compiled to [WebAssembly](webassembly.md) and exposes tools supplied by the application. A [restricted interpreter](restricted-interpreter.md) can also run Code Mode without Wasm.

## Checking tool calls

The script boundary can restrict which tools it can reach. Each [tool](tool.md) handler must still check whether the requested action is allowed. An issue lookup should check the project even if the script has no direct network access. See the [architecture survey](../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells) for other implementations.

[Back to Glossary](../glossary.md)
