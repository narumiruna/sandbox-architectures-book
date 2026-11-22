# Operating-system process sandboxes

An [operating-system process sandbox](../../glossary/operating-system-process-sandbox.md) lets an [agent](../../glossary/agent.md) use native commands on the [host](../../glossary/host.md) while restricting what those commands can reach. There is no separate operating system inside the sandbox.

## Who handles the request?

When the [Lamp](../../practice/design/from-issue-to-patch.md) test runner asks to open `total.c`, its [process](../../glossary/process.md) makes a [system call](../../glossary/system-call.md) to the host [kernel](../../glossary/kernel.md), which handles the request. On Linux, a [mount namespace](../../glossary/namespace.md) can give the process a view that includes the project but not the host's private directories. A [seccomp](../../glossary/seccomp.md) filter can block selected kinds of system calls, but it does not by itself enforce rules for individual file paths.

For example, [Anthropic Sandbox Runtime at revision `0bbebed0`](https://github.com/anthropic-experimental/sandbox-runtime/blob/0bbebed0aa9a8e628dc4df8bc30293550a1988eb/README.md) uses [Bubblewrap](https://github.com/containers/bubblewrap) on Linux and Seatbelt profiles on macOS. It also uses network proxies to check allowed destinations. The mechanisms differ by host platform; verify the behavior on the platform that will run the agent.

## What stays shared?

Processes inside and outside the sandbox use the same host kernel. The kernel can give each sandbox a different set of visible files, but a writable [mount](../../glossary/mount.md) of a host directory still lets the program change files in that directory.

## When to use it

Choose this boundary when a local agent needs native tools on the current operating system, but should not inherit unrestricted host access. This fits a test runner that uses the developer's existing command-line tools.

## What the boundary does not cover

Hiding files does not remove [credentials](../../glossary/credential.md) already given to the process, and a file rule does not restrict the network. Review inherited environment variables and open connections. [Verify the access rules](../../practice/verification/verifying-access-rules.md) with harmless files and a separate network check, and repeat the file check through a child process such as a test runner started by a package manager.
