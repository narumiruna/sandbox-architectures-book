# Observability

Observability is the ability to understand what a system did from evidence it records. A sandbox operator can use status changes, timestamps, or redacted logs to find which part of a job failed.

For example, a missing ready event and a workspace timeout point to provisioning. A compiler diagnostic after the worker became ready points to the build. Keep those records distinct so that a policy denial is not confused with a command error.

See [Observability and debugging](../practice/operations/observability-and-debugging.md).
