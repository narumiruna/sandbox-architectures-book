---
title: "gVisor Platforms"
source_type: "web"
url: "https://gvisor.dev/docs/architecture_guide/platforms/"
created: "2026-11-23"
updated: "2026-11-23"
---

# gVisor Platforms

[Original source](https://gvisor.dev/docs/architecture_guide/platforms/)

## Content

Describes how gVisor platforms handle system call interception and memory mapping. The KVM platform uses CPU virtualization without presenting a virtual hardware layer. The systrap platform uses Linux seccomp to intercept system calls without requiring CPU virtualization.
