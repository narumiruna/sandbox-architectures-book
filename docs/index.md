# Sandbox Architectures Book

A sandbox lets a program run while limiting what it can access. This book explains how sandboxes enforce those limits and how to choose a boundary for the code you need to run.

An AI agent that calls a few APIs needs a different environment from an agent that installs packages, builds software, and runs tests. The right choice starts with the work the agent must do, not with a product name.

## Start here

[Agent sandbox architectures](agent-sandbox-architectures.md) compares virtual machines, user-space kernels, operating-system process sandboxes, WebAssembly, engine isolates, and restricted interpreters. It also explains how control planes manage sandboxes without defining the isolation boundary.

As you compare designs, ask three questions:

1. **What must be isolated?** A tool script, a process, or an entire Linux workspace?
2. **What can cross the boundary?** Which files, network endpoints, credentials, and tools can the workload access?
3. **What stays after the run?** Which data survives in a workspace, snapshot, or cache?
