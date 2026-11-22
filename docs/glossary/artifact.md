# Artifact

An artifact is a selected output that a system keeps after a job, such as a patch, a test report, or a build result. It is not the entire [workspace](workspace.md).

For the Lamp task, a collector accepts the text patch and test output for review. The worker can be destroyed immediately; the review store keeps those files until their retention period ends. The reviewer treats both as untrusted output and must have permission to read them.

See [Workspaces and artifacts](../practice/data-and-access/workspaces-and-artifacts.md).
