# Sandbox lifecycle

Starting a worker and attaching a project's files are separate steps. Whether the worker boots, comes from a pool, or resumes saved state, it must receive the right workspace and restrictions before it can run. Destroying the worker does not delete outputs already sent for review.

**Illustrative example:** A read-only tool retrieves LAMP-17, a report that adding two item counts in Lamp gives the wrong total. A separate Linux worker compiles a tiny C program, runs tests, and returns a text patch and test output. It cannot publish.

## From create to destroy

All three startup paths lead to the same readiness check. Pausing keeps the current session; restoring here starts a new session from a clean template.

```mermaid
stateDiagram-v2
    accTitle: Lamp worker lifecycle
    accDescr: Creating a session selects cold boot, warm claim, or snapshot restore. Each path reaches Ready before running. An optional pause can resume. Running or paused workers can be destroyed. Retained outputs are deleted separately.
    state Start <<choice>>
    state "Cold boot" as Cold
    state "Warm claim" as Warm
    state "Snapshot restore" as Restore
    [*] --> Start: Create
    Start --> Cold
    Start --> Warm
    Start --> Restore
    Cold --> Ready
    Warm --> Ready
    Restore --> Ready
    Ready --> Running: Run
    Running --> Paused: Pause
    Paused --> Running: Resume
    Running --> Destroying: Stop
    Paused --> Destroying: Stop
    Destroying --> [*]
```

The [control plane](control-planes.md) also requests cleanup if startup fails or a ready worker is cancelled before running. The diagram omits these paths for clarity. Not every backend supports cold boot, pooling, restore, or pause.

Cold boot does the boot work after the request. A pool does it in advance and holds resources while workers wait. Restoring a snapshot with memory skips boot but still loads saved state. A disk-only snapshot restores files and still needs a boot. A pool can contain workers prepared by either boot or restore.

| State or action | Workspace and cache | Worker disk and memory | Access |
| --- | --- | --- | --- |
| Create | Select the Lamp revision; no project files attached yet. | Choose a startup path. | Authorize the request outside the worker. |
| [Cold boot](../../glossary/cold-boot.md) | No Lamp files; the base image can include compiler files. | Start with a clean disk layer and boot Linux with fresh memory. | No worker credentials. |
| [Warm claim](../../glossary/warm-pool.md) | Claim an unassigned worker with no project files or build cache. | Use the prepared worker's disk and live memory. | No worker credentials. |
| [Snapshot restore](../../glossary/snapshot.md) | Use a clean template without project files or build cache. | Resume from matching saved disk, memory, and machine state. | No credentials in the template; reset per-instance identity before use. |
| Ready | Confirm the disposable Lamp copy is attached and the build cache is empty. | The worker can accept the first command. | Check Lamp-only workspace access; no lookup or publish credentials in the worker. |
| Running | Write changes to the copy and cache. | Build writes stay on session storage; processes use live memory. | Enforce the same access rules for all worker commands. |
| Paused (optional) | Keep the copy and cache for this session only. | Keep the disk and hold suspended execution state in memory. | Recheck session authorization before resuming. |
| Destroying | Remove the copy and per-session cache. | Release worker memory and remove its disposable disk layer; keep clean base templates separate. | Close session access; the review store still checks its own access. |

The artifact collector exports only the patch and test output to a restricted review store. That store deletes those copies when retention expires, independently of worker cleanup. See [Workspaces and artifacts](../data-and-access/workspaces-and-artifacts.md).
