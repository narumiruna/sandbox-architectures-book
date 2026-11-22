# Container image

A container image is a package of files and settings that a [container runtime](container-runtime.md) uses to start a [container](container.md). It describes a starting environment, not the live state of a program.

## Example

A build service can reuse one image that contains a Python interpreter and project dependencies. Each new container can start with the same files. A report written by one build is not part of the original image and does not appear in another build unless the service saves or shares it separately.

## What the package contains

The [OCI Image Format v1.1.0](https://github.com/opencontainers/image-spec/blob/v1.1.0/manifest.md) describes an image through a *manifest* that references configuration and filesystem layers. The configuration can supply default settings, such as the command to run. The layers describe filesystem changes that image tooling applies in order to prepare the container's starting files.

An image neither preserves running processes like a memory [snapshot](snapshot.md) nor decides how the workload is isolated. The same compatible image can run under different runtimes. Check the runtime and its policy to learn what the code can reach.

[Back to Glossary](../glossary.md)
