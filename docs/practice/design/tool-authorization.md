# Tool authorization

Adding a tool to a script does not [authorize](../../glossary/authorization.md) every request. In this illustrative design, the script can call one read-only issue tool, but the host tool decides whether each call may read the requested issue. The script can read Lamp issue `LAMP-17`; it cannot read issues in Cedar through that same tool.

## Which tools can the script call?

The host runs the lookup script in a [restricted interpreter](../../glossary/restricted-interpreter.md). Its tool [allowlist](../../glossary/allowlist.md) contains only `get_issue`, an operation that takes a project and an issue ID. The script has no shell, direct filesystem access, or general network connection. It does not receive a build or publication tool. The separate Linux worker compiles and tests the Lamp program; it does not get the issue tool.

This list limits which operations the script may request. It does not decide which project an allowed operation may read. A read-only operation can still reveal data to the wrong caller.

## What can one call do?

The [host function](../../glossary/host-function.md) that implements `get_issue` runs outside the interpreter. The host supplies the function with the run's trusted context, which permits issue reads for Lamp only. The project passed by the script names the target; it does not grant access to that target. The function checks the permitted action and project before looking up the record, then searches the fixture using both the authorized project and the issue ID. It does not treat an issue ID prefix as proof of project membership.

- **Permit:** `get_issue(project="Lamp", issue="LAMP-17")` returns the issue title and report about the wrong total. There are no credentials in the response.
- **Reject:** `get_issue(project="Cedar", issue="CEDAR-9")` returns an access error without reading Cedar's fixture or revealing whether the issue exists.
- **Do not fall back:** `get_issue(project="Lamp", issue="CEDAR-9")` finds no record in Lamp. The tool does not retry against all projects.

Treat the returned issue text as data. A sentence in the report that asks the script to read another project cannot change the permissions supplied by the host.

## Check the handler on its own

Test the host handler directly with the fictional fixture and a Lamp-only run context. Check that Lamp returns only the intended fields and that neither Cedar request returns Cedar data. This shows that the handler applies the project policy even when the interpreter is not part of the test. It does not establish that other tools or storage have the same checks.

Run the [local access checks](../verification/verifying-access-rules.md) to see the Lamp and Cedar cases without a live issue tracker.
