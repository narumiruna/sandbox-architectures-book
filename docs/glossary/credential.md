# Credential

A credential is something a service uses to verify who is asking or what access they have. An API token, for example, is a value a program can send to a service to get access. If sandbox code receives a reusable credential, it may be able to use it beyond the one action you intended.

## Example

A sandbox needs the title of an issue. A [tool](tool.md) running outside the sandbox checks that the issue belongs to the approved project. The tool sends a read-only token to the issue tracker and returns the title to the sandbox. The tool and tracker handle the token; the sandbox code receives only the title.

## Who can use it

Anyone who obtains a valid [bearer token](https://www.rfc-editor.org/rfc/rfc6750.html#section-1.2) can use it where the service accepts it. If sandbox code can read the token from a file or a program setting, it can use the token directly. Copies can also end up in logs or in a [snapshot](snapshot.md) that saves the program's memory.

Use [least privilege](least-privilege.md): prefer a short-lived credential that grants access only to the operations and resources needed for the task. When the code needs the result rather than the credential, a host tool or [credential injection](credential-injection.md) can keep the credential out of the program.

[Back to Glossary](index.md)
