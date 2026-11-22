# Open Container Initiative (OCI)

The [Open Container Initiative](https://opencontainers.org/) maintains open specifications for packaging, distributing, and running containers. OCI compatibility helps different tools work together. It does not tell you what separates the running program from the host.

## Example

A build service packages its compiler and test tools as an OCI [container image](container-image.md). It can use the same image to start a test sandbox with either a shared host kernel or a [virtual machine](virtual-machine.md), if both backends support the image and its programs.

## What each specification covers

The [Image Specification v1.1.0](https://github.com/opencontainers/image-spec/tree/v1.1.0) defines the package of filesystem changes and settings. The [Distribution Specification v1.1.0](https://github.com/opencontainers/distribution-spec/tree/v1.1.0) defines how tools transfer content to and from a registry, a service that stores container images. The [Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/tree/v1.2.1) defines the configuration and lifecycle for running a prepared container. To learn what the code can reach, check the selected [container runtime](container-runtime.md) and its settings.

[Back to Glossary](index.md)
