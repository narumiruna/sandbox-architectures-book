# Warm pool

A warm pool is a set of [sandboxes](sandbox.md) prepared before requests arrive. A request can claim one without waiting for all the setup. How much work is already done varies by platform; a prepared sandbox may still need request-specific setup.

## Example

A build service keeps three unassigned Linux sandboxes with the compiler installed and its command service running. A request claims one, attaches its project files, and starts the build. If all three have been claimed, another request may wait or incur a [cold start](cold-start.md).

## Prepared instances, not saved files

The [control plane](control-plane.md) prepares instances, assigns them to requests, and can refill the pool. For example, [Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/examples/warmpool-quickstart/README.md) describes a `SandboxWarmPool` that prepares instances and a `SandboxClaim` that adopts one. That lifecycle mechanism does not determine how the sandbox isolates its workload.

A [snapshot](snapshot.md) is saved state. A service can restore snapshots to refill a warm pool, but keeping only snapshots still leaves restore work when a request arrives. A pool moves work earlier at the cost of holding resources while instances wait. Keep [tenant](tenant.md) data out of unassigned instances, and account for assignment and workspace setup when measuring readiness.

[Back to Glossary](index.md)
