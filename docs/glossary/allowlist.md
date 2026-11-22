# Allowlist

An allowlist names the resources a program may use or the actions it may take. It limits access only if a trusted component checks requests and blocks those that do not match.

## Example

A build sandbox needs to download software packages. Its [policy](policy.md) allows [egress](egress.md) connections only to the team's package mirror, a server that stores copies of those packages. The network control that checks each new connection enforces the list; the list alone does not block traffic.

## What a rule can match

The scope depends on what the component doing the checks can see. A connection rule may match a destination and a port. A service that forwards and reads web requests can also check the operation and path. The [OpenShell v0.1.9 network rules](https://github.com/NVIDIA/OpenShell/blob/v0.1.9/docs/how-it-works/policies/network-rules.mdx#connection-and-request-checks) illustrate these two levels of checks.

Allowing a connection to a service does not limit what the workload can send to it or what actions the service will accept. For [least privilege](least-privilege.md), match the action as well as the destination when the workload needs only one operation. Make sure the restricted access goes through the component that enforces the rule; a check on one path does not cover other paths.

[Back to Glossary](index.md)
