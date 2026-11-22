# Workload

A workload is the code and processes that an environment runs for a task. In a sandbox it could be one script, a build with several processes, or an entire agent session. The workload is what runs, not the package it starts from or the service that starts it.

## Example

An [agent](agent.md) runs a generated script in one [sandbox](sandbox.md) to decide which tests to run. A tool then starts the test runner and its helper processes in a separate Linux sandbox. The script is the first workload; the test runner and its helpers make up the second. The agent does not have to run inside either sandbox.

## Choosing a boundary for the work

Different workloads need different execution environments. A script that combines results from tools may need only a [restricted interpreter](restricted-interpreter.md). A build that launches [native binaries](native-binary.md), programs compiled for a particular machine and operating system, needs a compatible environment that can run them.

A [container image](container-image.md) supplies starting files and settings; it is not the running workload. Check where the workload's child processes actually run, which resources they can reach, and whether several workloads share one [isolation unit](isolation-unit.md). See [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md) for environments that fit different kinds of work.

[Back to Glossary](index.md)
