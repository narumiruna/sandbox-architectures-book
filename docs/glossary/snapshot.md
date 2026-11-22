# Snapshot

A snapshot is saved state that a system can restore later. A disk-only snapshot preserves storage, not running programs. A snapshot with memory can preserve running state when it also includes the necessary processor and device state. Saved memory can contain [credentials](credential.md) and other secrets, so treat it as sensitive data.

## Example

A test service boots a Linux sandbox and saves a template before assigning it to a user. With a disk-only snapshot it can reuse the prepared files but must boot Linux and start its services. With a snapshot of the running VM it can resume those services from the saved point. In either case, the service still has to set up the user's workspace and access for the new session.

## What the restore can recover

Check which files and external resources the snapshot actually preserves. For example, [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/snapshotting/snapshot-support.md#overview) writes separate guest memory and VM state files. The operator manages the backing disks, and existing network connections are not guaranteed to survive. Check that the restore environment is compatible and that it has the matching disk state.

When several VMs resume from one memory snapshot, they can inherit identifiers or other values meant to be unique. The 2021 preprint [Restoring Uniqueness in MicroVM Snapshots](https://arxiv.org/abs/2102.12892) explains why restored instances need fresh per-instance state. Keep user-specific data and secrets out of shared templates. Disk snapshots can also contain secrets written to files.

A snapshot is a saved artifact, not a [warm pool](warm-pool.md) of prepared sandboxes. A service can use snapshots to fill a pool or restore one when a [cold start](cold-start.md) is necessary.

[Back to Glossary](index.md)
