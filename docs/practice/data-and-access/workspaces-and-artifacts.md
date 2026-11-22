# Workspaces and artifacts

Let the worker edit a copy of the project and return only the files the reviewer needs. In this illustrative design, `LAMP-17` reports that adding two item counts gives the wrong total in project Lamp. A read-only issue tool retrieves the report. A separate Linux worker builds and tests a fix in `/work`. It returns a text patch and test output for review, but cannot publish the fix.

## Choose what the worker can change

A [workspace](../../glossary/workspace.md) is the set of files a job can work with. A [mount](../../glossary/mount.md) makes files available at a path; it does not necessarily copy them. A checkout is the source tree at a selected repository revision.

| Workspace choice | Effect on the original checkout | When it fits |
| --- | --- | --- |
| Read-only mount | The worker can read the files but cannot change them through that mount. Edits need a separate writable location. Other processes may still change the original. | Inspection, or a build that writes all output elsewhere. |
| Writable shared directory | If the directory is the original checkout, edits, deletions, and partial writes change the original as they happen, even if the job fails. | A trusted local workflow where live edits are intentional. |
| Disposable copy with explicit export | The worker edits only its copy. The original is not mounted, and the worker has no other path to write it. Nothing returns unless a separate collector accepts it. | A build that needs to edit source but must not apply changes before review. |

Read-only does not mean private: the worker can still read everything exposed by the mount. With any choice, give it only the inputs it needs. Do not include local settings or [credentials](../../glossary/credential.md).

## Decide what leaves `/work`

[Artifacts](../../glossary/artifact.md) are selected outputs kept after a job. The Lamp reviewer needs only two: the patch and the test output.

1. The [control plane](../../glossary/control-plane.md) prepares the needed Lamp source files and tests at a known revision. The worker edits its copy, compiles the tiny C program, and runs the tests there.
2. A collector outside the worker boundary accepts only the two named text files. It sets size limits, does not follow filesystem links, and records the source revision and job status separately from the worker's text. Only an authorized Lamp reviewer can read the files. They are untrusted text: a log that says the tests passed is not approval to apply the patch.
3. After collection, or when collection fails, the control plane discards `/work`, including changed source, the compiled program, and temporary files. The review store keeps the accepted artifacts for a limited time. Applying the patch or publishing it is a separate action outside the worker.

File access is only one part of the design. The [network policy](network-policy.md) controls whether the worker can send or receive data over the network.
