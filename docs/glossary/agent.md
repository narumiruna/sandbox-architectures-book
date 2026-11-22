# Agent

An agent is a system that uses an AI model to decide what to do next and can call tools to act. An agent can ask a model to write a script, but the script is only one piece of work the agent may run. Putting that script in a sandbox does not put the rest of the agent in the same sandbox.

## Example

An agent prepares a project status report. It asks its model to write a script that looks up issue titles and groups them by label. The script runs in a [sandbox](sandbox.md) that can call only the issue lookup [tool](tool.md). The application that calls the model and the service that handles issue lookups both run outside that script sandbox.

## What the agent runs

The agent can give the model a task, run a requested tool, and feed the result back to the model for its next decision. It can request one tool call at a time or use [Code Mode](code-mode.md) to let a generated script make several calls and combine their results.

A different design runs the agent application itself inside a sandbox, along with the local commands it launches. To tell the two designs apart, ask which code is the [workload](workload.md) at each [isolation boundary](isolation-boundary.md). A tool handler outside a boundary uses its own permissions, even when the request came from inside it.

[Back to Glossary](../glossary.md)
