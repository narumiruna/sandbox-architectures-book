# Workspace

A workspace is the set of files a job can work with. It can be a copied checkout, a mounted directory, or a combination of inputs and writable scratch space.

For example, a worker can edit a disposable copy of the Lamp project while the original checkout stays outside the sandbox. A writable [mount](mount.md) has a different effect: writes to the mount may change the original files.

See [Workspaces and artifacts](../practice/data-and-access/workspaces-and-artifacts.md).
