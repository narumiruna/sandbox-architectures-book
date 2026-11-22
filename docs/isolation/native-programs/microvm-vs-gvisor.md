# MicroVM vs gVisor

Start with one question: **Does the job need its own Linux kernel?** If yes, start with a [microVM](microvm.md) whose guest kernel and devices meet the requirements. If no, [gVisor](gvisor.md) is a candidate for a compatible Linux [container](../../glossary/container.md). A microVM is a kind of [virtual machine](../../glossary/virtual-machine.md); gVisor is one implementation of a [user-space kernel](../../glossary/user-space-kernel.md). The names alone do not tell you which is safer or faster for your deployment.

## Compare the execution boundaries

When a program asks to open a file, the key difference is [which component answers the request](../../sandbox-isolation-boundaries.md#sandboxes-for-operating-system-workloads). Either boundary can expose the same project files if configured to do so.

| What to check | MicroVM | gVisor |
| --- | --- | --- |
| Who handles Linux [system calls](../../glossary/system-call.md)? | A Linux [guest kernel](../../glossary/guest.md) running inside the VM. | The [Sentry](https://gvisor.dev/docs/architecture_guide/intro/#how-does-gvisor-provide-isolation), even on the KVM platform. |
| What must the [host](../../glossary/host.md) provide? | A supported virtualization backend for a hardware-backed microVM. For example, [Firecracker v1.11.0 uses KVM](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#internal-architecture). | A supported Linux host. [systrap does not require hardware virtualization](https://gvisor.dev/docs/architecture_guide/intro/#how-does-gvisor-provide-isolation); [the KVM platform uses it](https://gvisor.dev/docs/architecture_guide/platforms/#kvm). |
| What can the job depend on? | The interfaces of the chosen guest kernel and the devices the VM exposes. | The [Linux interfaces gVisor implements](https://gvisor.dev/docs/user_guide/compatibility/) and the resources the runtime exposes. |
| Which jobs share a boundary? | Jobs assigned to one microVM share its guest kernel. | Jobs assigned to one gVisor sandbox share its Sentry. |

## Make the choice with one real job

1. **Check the hard requirement.** If a test verifies behavior of a particular Linux kernel build, use a microVM that can boot that build. If the job only compiles and tests a user-space program from a container image, try gVisor as well. Passing a smoke test is not enough; run the install, build, and tests.
2. **Check the same access rules in both.** Use the same project revision and give each job only its intended files, network destinations, and credentials. Check which jobs share one sandbox and what can carry over to the next run. These are separate decisions from the mechanism shown in the table.
3. **Measure only candidates that meet the requirements.** Record the runtime version, platform, and whether you start fresh, restore saved state, or claim a ready sandbox. [Measure](../../practice/verification/measuring-a-sandbox.md) time to the first usable command, time to finish the job, and host memory under the expected concurrency. Do not compare a cold launch on one side with a ready worker on the other and attribute the difference to isolation alone.

For an existing system that offers both options, see [Agent Substrate's architecture](../../agent-substrate.md).
