# Egress

Egress는 sandbox의 경계를 넘어 외부로 나가는 네트워크 트래픽이다. Egress [policy](policy.md)는 sandbox가 연결할 수 있는 외부 서비스를 제한할 수 있다. 서비스에 연결할 수 있다는 사실만으로는 sandbox가 그 서비스에서 수행할 수 있는 작업이 제한되지 않는다.

## 예시

Sandbox는 테스트 서버의 샘플 레코드를 읽는 테스트를 실행한다. Gateway는 sandbox가 해당 레코드를 읽도록 허용하지만, 레코드를 변경하거나 다른 서비스에 연결하려는 요청은 차단한다. 요청은 sandbox 밖으로 나가고 응답은 다시 sandbox 안으로 들어온다.

## 외부로 나가는 트래픽에 규칙을 적용하는 위치

Firewall은 네트워크 주소와 포트의 [allowlist](allowlist.md)를 적용할 수 있다. 규칙이 읽기와 쓰기를 구분해야 한다면 web proxy처럼 요청을 읽을 수 있는 구성 요소를 사용하거나, 서비스 자체에서 작업을 제한한다. 신뢰할 수 있는 구성 요소가 해당 경로에서 규칙을 적용해야 한다. Proxy 설정만으로는 직접 연결을 제한할 수 없다.

네트워크 접근과 [tool](tool.md)이 제공하는 작업은 별도로 확인한다. 직접 네트워크에 접근할 수 없더라도 sandbox는 자신을 대신해 요청을 보내는 host tool을 호출할 수 있다. 그런 tool에는 별도의 authorization이 필요하다.

## 연결과 응답

외부로 나간 요청에 대한 응답은 sandbox 안으로 들어오므로 [ingress](ingress.md) 트래픽이다. 네트워크 제어는 외부 클라이언트가 새 연결을 시작하지 못하게 하면서도 sandbox가 시작한 연결의 응답은 허용할 수 있다. 클러스터의 네트워크 소프트웨어가 [Kubernetes 1.35 network policies](https://github.com/kubernetes/website/blob/03c191bcc446f9c15a9e68d6cd1154b53bde4291/content/en/docs/concepts/services-networking/network-policies.md#the-two-sorts-of-pod-isolation)를 적용하면 이와 같이 동작한다.

[용어집으로 돌아가기](index.md)
