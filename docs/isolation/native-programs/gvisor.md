# gVisor

[gVisor](https://gvisor.dev/docs/architecture_guide/intro/) runs Linux [containers](../../glossary/container.md) without booting a separate Linux [guest kernel](../../glossary/guest.md). Its [user-space kernel](../../glossary/user-space-kernel.md), the **Sentry**, handles requests from the programs inside the sandbox. The trade-off is compatibility: gVisor implements the Linux interface itself, so some features are missing or behave differently.

## Where the file request goes

1. The [Lamp](../../practice/design/from-issue-to-patch.md) test runner makes a [system call](../../glossary/system-call.md) to open `total.c`. The Sentry handles the call in the sandbox's filesystem view; it does not pass the workload's call directly to the [host](../../glossary/host.md) kernel.
2. When configured to expose host files, gVisor can use a helper process called the **Gofer** to [provide access to those mounts](https://gvisor.dev/docs/user_guide/filesystem/). Depending on configuration, the Gofer can let the Sentry perform file operations directly on exposed files rather than handle each operation itself. gVisor still relies on the host kernel for underlying resources. Hiding the rest of the host does not hide a file deliberately mounted into the sandbox.

## What changes with the platform?

The gVisor [platform](https://gvisor.dev/docs/architecture_guide/platforms/) is the mechanism that lets the Sentry intercept calls and manage how programs run. **systrap** does not need CPU virtualization support. The **KVM** platform uses [hardware virtualization](hardware-backed-virtual-machines.md), but the Sentry still provides the Linux interface. Using KVM does not make gVisor a [microVM](microvm.md) that boots its own Linux kernel.

## What to verify before choosing gVisor

- **Runtime:** gVisor provides `runsc`, an [OCI](../../glossary/open-container-initiative.md) [container runtime](../../glossary/container-runtime.md). Verify that your deployment selects it for the job; a container image alone does not select the boundary.
- **Compatibility:** Check the [supported Linux features](https://gvisor.dev/docs/user_guide/compatibility/). For example, gVisor does not support mounting a native block device from inside the sandbox. Run the full job, including setup and tests. A shell that starts does not prove the build works.
- **Sharing:** Programs in the same gVisor sandbox share its Sentry. Decide which jobs may share a sandbox instance, then [verify the access rules](../../practice/verification/verifying-access-rules.md) for mounts, network access, and credentials.

See [MicroVM vs gVisor](microvm-vs-gvisor.md) for a decision guide.
