# Container runtime

A container runtime is software that sets up and runs a [container](container.md). It applies the chosen isolation settings and starts the programs. Two runtimes can start from the same [container image](container-image.md) but give the programs different boundaries.

## Example

A build service asks a runtime to start a sandbox for a test job. The runtime makes the project available at `/workspace` and starts the test runner. The service decides when and where to run the job; the runtime sets up the environment in which it runs.

## From packaged files to a running process

A container stack can unpack an image's files and combine them with runtime settings to prepare a *bundle*: the local files and settings needed to start the workload. The [OCI Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/tree/v1.2.1) defines the bundle and lifecycle operations such as create and start. A low-level runtime can take a prepared bundle without downloading the image itself.

## Where the kernel interface comes from

A runtime can use the [host kernel](kernel.md) directly with [namespaces](namespace.md), provide a [user-space kernel](user-space-kernel.md), or run the workload in a [virtual machine](virtual-machine.md) with its own kernel. The [control plane](control-plane.md) manages the workload; the runtime's execution mechanism and settings determine what separates it from the host.

[Back to Glossary](../glossary.md)
