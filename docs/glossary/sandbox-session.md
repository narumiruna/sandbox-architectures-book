# Sandbox session

A sandbox session is a run or period of use tracked as one unit by a [sandbox](sandbox.md) service. The service may keep a [workspace](workspace.md) and worker state for several requests in one session.

## Example

A Lamp session includes one request to edit the source and another to run tests. During the session, the test runner can see the changes from the edit. When the service closes the session it can discard the workspace and still keep the test report as an [artifact](artifact.md).

## When it matters

When reusing a session across requests, check which files and state survive pause, resume, and cleanup. Closing a session can stop commands and release the worker without deleting outputs in a separate store.

See [Sandbox lifecycle](../practice/operations/sandbox-lifecycle.md).
