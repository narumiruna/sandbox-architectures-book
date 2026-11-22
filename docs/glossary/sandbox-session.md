# Sandbox session

A sandbox session is a run or period of use tracked as one unit by a sandbox service. The service may keep a workspace and worker state for several requests in one session.

Closing the session can stop commands and release the worker. It does not necessarily delete outputs in a separate store. Check which files and state survive each transition, including pause, resume, and cleanup.

See [Sandbox lifecycle](../practice/operations/sandbox-lifecycle.md).
