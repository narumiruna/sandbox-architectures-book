# Tool

A tool is an operation that an agent or a script can request, such as looking up an issue or starting a build. The caller supplies inputs, and a component called the handler performs the operation. Being allowed to call a tool does not mean every request to that tool should be allowed.

## Example

A release script runs in a [sandbox](sandbox.md) and calls a tool to retrieve the title of an issue. The script supplies the issue number. The handler checks that the issue belongs to the project the script may read and returns only the title. The handler can use the issue service without handing the script its [credential](credential.md).

## The interface and the handler

The tool interface describes what the caller can request. In a language sandbox, a [host function](host-function.md) can provide a route from the script to the handler. The handler enforces [policy](policy.md): it checks whether the caller can perform the operation on the resource, then limits the effects and results to that scope. A valid issue number has the right format; it is not proof that the caller may read that issue.

The sandbox can limit which tools a script can call, but it cannot impose the script's restrictions on a handler that runs outside it. A build tool can start a job in a separate sandbox suited to that [workload](workload.md). The script boundary and the build boundary then protect different parts of the system.

[Back to Glossary](index.md)
