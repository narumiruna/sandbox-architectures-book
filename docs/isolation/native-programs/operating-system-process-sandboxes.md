# Operating-system process sandboxes

A [process sandbox](../../glossary/operating-system-process-sandbox.md) lets an agent use native commands on the host while restricting what those commands can reach. The process still uses the host operating-system kernel. There is no separate guest kernel or reimplementation of the Linux interface.

## Where the boundary is

Suppose a local agent starts a test runner. The test runner can read the project files it needs, but the operating system can deny access to a directory outside the project. On Linux, a [mount namespace](../../glossary/namespace.md) can give a process a limited view of the filesystem. A [seccomp](../../glossary/seccomp.md) filter can block selected kinds of system calls, but it does not by itself enforce rules for individual file paths.

For example, [Anthropic Sandbox Runtime at revision `0bbebed0`](https://github.com/anthropic-experimental/sandbox-runtime/blob/0bbebed0aa9a8e628dc4df8bc30293550a1988eb/README.md) uses bubblewrap on Linux and Seatbelt profiles on macOS. It also uses network proxies to check allowed destinations. The mechanisms differ by host platform; verify the behavior on the platform that will run the agent.

## When to use it

Choose this boundary when a local agent needs the developer's existing tools but should not inherit unrestricted host access.

1. Use a harmless test file inside the workspace and another outside it. Verify that the intended file is accessible and the other is not.
2. Repeat the check through a child process, such as a test runner started by a package manager.
3. Verify network restrictions separately. Also review which environment variables and open connections the agent can inherit; hiding files does not remove credentials already passed to a process.
