# Authorization

Authorization is deciding whether a known caller may perform an action on a specific resource. Establishing who the caller is comes first; knowing their identity does not grant access.

## Example

A script can call an issue lookup [tool](tool.md) to read `LAMP-17` but cannot read another project's issues. The tool checks the known caller's permissions and the requested issue on every request. A request field naming another project is not proof of permission.

## When it matters

Check authorization when an operation can return data or make changes on behalf of a caller. A [sandbox](sandbox.md) may limit which tools a script can call, but each tool still needs to check what that caller may do. See [Tool authorization](../practice/design/tool-authorization.md) for a worked example.

[Back to Glossary](index.md)
