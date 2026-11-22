# Egress

Egress is network traffic that leaves a sandbox across its boundary. An egress [policy](policy.md) can restrict which outside services the sandbox can contact. Permission to reach a service does not by itself limit what the sandbox can do there.

## Example

A sandbox runs tests that read sample records from a test server. A gateway lets it read those records but blocks requests to change them or contact other services. The request leaves the sandbox and the reply comes back in.

## Where outbound rules apply

A firewall can enforce an [allowlist](allowlist.md) of network addresses and ports. If a rule needs to distinguish a read from a write, use a component that can read the request, such as a web proxy, or limit the operation at the service itself. A trusted component must enforce the rule on the relevant path; a proxy setting alone does not constrain direct connections.

Check network access separately from the operations exposed through a [tool](tool.md). Even without direct network access, a sandbox may be able to call a host tool that makes requests on its behalf. That tool needs its own authorization.

## Connections and replies

Replies to an outbound request are [ingress](ingress.md) traffic because they enter the sandbox. A network control can allow replies on connections the sandbox started without letting outside clients start new connections. [Kubernetes 1.35 network policies](https://github.com/kubernetes/website/blob/03c191bcc446f9c15a9e68d6cd1154b53bde4291/content/en/docs/concepts/services-networking/network-policies.md#the-two-sorts-of-pod-isolation) work this way when the cluster's networking software enforces them.

[Back to Glossary](../glossary.md)
