# Sandbox Architectures Book

A [sandbox](glossary/sandbox.md) lets a program run while limiting what it can access. This book explains how sandboxes enforce those limits and how to choose a boundary for the code you need to run.

An AI agent that calls a few APIs needs a different environment from an agent that installs packages, builds software, and runs tests. The right choice starts with the work the agent must do, not with a product name.

## Start here

Start with **Foundations**, then follow Lamp, a fictional coding task, through the four practical parts. If you already know the isolation mechanisms, start with the worked example in **Design a sandbox**.

1. **Foundations.** [Sandbox isolation boundaries](sandbox-isolation-boundaries.md) explains what enforces access limits. Explore six ways to run operating-system workloads or code in a language or module runtime.
2. **Design a sandbox.** [From issue to patch](practice/design/from-issue-to-patch.md) follows Lamp from issue lookup to human review. Then [choose a sandbox](practice/design/choosing-a-sandbox.md) and decide [where to run it and who operates it](practice/design/deployment-patterns.md).
3. **Set access rules.** Start with [tool authorization](practice/design/tool-authorization.md), then decide which files, network endpoints, and credentials each part of the task can use. Keep different customers' or teams' work and data separate.
4. **Operate a sandbox.** Start with [control planes](practice/operations/control-planes.md) to see who starts and cleans up the worker. Then learn how to manage its lifetime, limit its resource use, and diagnose failures.
5. **Verify a sandbox.** [Check that access rules work](practice/verification/verifying-access-rules.md), then [measure the task](practice/verification/measuring-a-sandbox.md). The local labs demonstrate the method, not the safety or speed of a production setup.

## Use the reference

- [Agent sandbox architectures](agent-sandbox-architectures.md) compares real implementations. Use it to find candidates after you know what boundary your workload needs.
- [Glossary](glossary.md) defines unfamiliar terms and links to detailed explanations.

## Questions to carry through the book

1. **What must be isolated?** A tool script, a process, or an entire Linux workspace?
2. **What can cross the boundary?** Which files, network endpoints, credentials, and tools can the workload access?
3. **What stays after the run?** Which data survives in a workspace, snapshot, or cache?
