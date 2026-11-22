# Workspaces and artifacts

Let the worker edit a copy of the project and return only the files the reviewer needs. In the [Lamp walkthrough](../design/from-issue-to-patch.md), the Linux worker builds and tests a fix in `/work`. It can return a text patch and test output for review, but it cannot publish the fix.

## Choose what the worker can change

A [workspace](../../glossary/workspace.md) is the set of files a job can work with. A [mount](../../glossary/mount.md) makes files available at a path; it does not necessarily copy them. A checkout is the source tree at a selected repository revision.

| Workspace choice | Effect on the original checkout | When it fits |
| --- | --- | --- |
| Read-only mount | The worker can read the files but cannot change them through that mount. Edits need a separate writable location. Other processes may still change the original. | Inspection, or a build that writes all output elsewhere. |
| Writable shared directory | If the directory is the original checkout, edits, deletions, and partial writes change the original as they happen, even if the job fails. | A trusted local workflow where live edits are intentional. |
| Disposable copy with explicit export | The worker edits only its copy. The original is not mounted, and the worker has no other path to write it. Nothing returns unless a separate collector accepts it. | A build that needs to edit source but must not apply changes before review. |

Read-only does not mean private: the worker can still read everything exposed by the mount. With any choice, give it only the inputs it needs. Do not include local settings or [credentials](../../glossary/credential.md).

## Decide what leaves `/work`

[Artifacts](../../glossary/artifact.md) are selected outputs kept after a job. The Lamp reviewer needs only two: `change.patch` (128 KiB max) and `test.log` (64 KiB max). These example caps apply to the accepted files, separately from the worker's disk limit.

1. The workspace service follows the run assignment from the [control plane](../../glossary/control-plane.md). It copies the approved revision's source and tests and the task summary to a fresh [guest](../../glossary/guest.md) disk mounted at `/work`. It does not copy repository history, settings, or secrets, and does not mount the original checkout. The worker can change the copy, including the tests.
2. After the build and test commands report success and the worker stops, a collector outside the worker's [isolation boundary](../../glossary/isolation-boundary.md) reads only the two named files from that run's disk. It accepts the pair only if both are regular UTF-8 text files within the limits, without following filesystem links. It rejects missing, oversized, or invalid results instead of exposing partial output. It uses the run ID, base revision, and attempt status from the control plane rather than trusting worker-provided labels.
3. The review store accepts uploads only from the collector and permits reads only for the designated Lamp reviewer of that run. Being a requester does not automatically grant review access. The store presents the two files as untrusted text, never as commands or approval to apply the patch. It removes both copies seven days after acceptance. In this example, there are no secondary copies in backups.
4. The workspace service discards `/work`, including changed source, binaries, and temporary files, even if export fails. The [control plane verifies that cleanup](../operations/sandbox-lifecycle.md#what-gets-deleted-and-when); expiry in the review store is separate.

Checking filenames and sizes does not check what the text says. The worker can put any data it can read into either file. Leave secrets and unrelated data out of the workspace in the first place.

Next: [Network policy](network-policy.md) explains why the worker can exchange those files without getting access to network services.
