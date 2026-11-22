# Authorization

Authorization is deciding whether a known caller may perform an action on a specific resource. Establishing who the caller is comes first; knowing their identity does not grant access.

An issue tool might accept calls from a script but limit that script's read access to the Lamp project. The tool checks the caller's permissions and the target issue on every request. A request field naming another project is not proof of permission.

See [Tool authorization](../practice/design/tool-authorization.md).
