# Tool authorization

A [tool](../../glossary/tool.md) can be available to a script without every call being [authorized](../../glossary/authorization.md). In the [Lamp walkthrough](from-issue-to-patch.md), the script can call one read-only issue tool, but the [host](../../glossary/host.md) checks each request. The script can read Lamp issue `LAMP-17`, not other Lamp issues or issues in Cedar.

## Which tools can the script call?

The host runs the lookup script in a [restricted interpreter](../../glossary/restricted-interpreter.md). Its tool [allowlist](../../glossary/allowlist.md) contains only `get_issue`, an operation that takes a project and an issue ID. The script has no shell, direct filesystem access, or general network connection. It does not receive a build or publication tool. The separate Linux worker compiles and tests the Lamp program; it does not get the issue tool.

This list limits which operations the script may request. It does not decide which project an allowed operation may read. A read-only operation can still reveal data to the wrong caller.

## What can one call do?

The [host function](../../glossary/host-function.md) that implements `get_issue` runs outside the interpreter. The host supplies the function with the scope already approved for this run: read Lamp's `LAMP-17`. The script's arguments name the target; they do not grant access. The handler checks the permitted action, project, and issue before looking up the record. It reads the local fixture using both the authorized project and the issue ID. An issue ID prefix is not proof of project membership.

- **Permit:** `get_issue(project="Lamp", issue="LAMP-17")` returns only the issue title and report about the wrong total. It returns no [credentials](../../glossary/credential.md) or other records.
- **Reject:** `get_issue(project="Cedar", issue="CEDAR-9")` fails the project check, without reading Cedar's fixture or revealing whether the issue exists.
- **Do not fall back:** `get_issue(project="Lamp", issue="CEDAR-9")` fails the run's issue check. If the tool is configured for project-wide reads instead, it must still search only Lamp and return no match; it must not retry against all projects.

Treat the returned issue text as data. A sentence in the report that asks the script to read another project cannot change the permissions supplied by the host.

## Check the handler on its own

Test the host handler directly with dummy records for both projects and a context that permits only Lamp's `LAMP-17`. Check that the allowed call returns only the intended fields and that another issue in either project is rejected before lookup. That tests this handler independently of the interpreter, not the access checks at other interfaces. The [local access checks](../verification/verifying-access-rules.md) demonstrate the simpler project-wide rule, without a live issue tracker.

Next: [Workspaces and artifacts](../data-and-access/workspaces-and-artifacts.md) follows the source copy into the worker and the two text files out.
