# Ingress

Ingress is network traffic that enters a sandbox across its boundary. An ingress [policy](policy.md) can control who may start a connection to a service inside. A preview URL gives a browser a route to a service, but it does not by itself verify who is using it.

## Example

A developer starts a web server in a sandbox and opens a preview of the site. A gateway outside the sandbox checks the developer's sign-in and whether they have access to that sandbox. It forwards requests only to the preview web server and does not pass the sign-in [credential](credential.md) to the sandbox.

## Routing and access checks

A gateway can act as a *reverse proxy*: it accepts web requests from clients and forwards them to the selected server, as described in [RFC 9110, Section 3.7](https://www.rfc-editor.org/rfc/rfc9110.html#section-3.7). Routing chooses the sandbox and service. Authorization checks whether the caller is allowed to reach them. To enforce that decision at the gateway, make the service reachable only through that checked route.

Check what the route exposes and when it closes. A preview route need not expose other services in the sandbox, and it should close when the session ends. Replies from the preview server leave the sandbox as [egress](egress.md) traffic, even though the outside client started the connection.

[Back to Glossary](../glossary.md)
