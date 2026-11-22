# Ingress

Ingress는 sandbox의 경계를 넘어 안으로 들어오는 네트워크 트래픽이다. ingress [policy](policy.md)는 누가 내부 서비스에 연결을 시작할 수 있는지 제어할 수 있다. 미리보기 URL은 브라우저에 서비스로 가는 경로를 제공하지만, 그 자체로는 누가 그 경로를 사용하는지 확인하지 않는다.

## 예시

개발자가 sandbox에서 웹 서버를 시작하고 사이트 미리보기를 연다. sandbox 외부의 gateway는 개발자의 로그인 여부와 해당 sandbox에 접근할 권한이 있는지 확인한다. gateway는 요청을 미리보기 웹 서버에만 전달하며 로그인 [credential](credential.md)은 sandbox에 전달하지 않는다.

## 라우팅과 접근 확인

[RFC 9110, Section 3.7](https://www.rfc-editor.org/rfc/rfc9110.html#section-3.7)에서 설명하듯, gateway는 *reverse proxy* 역할을 할 수 있다. 즉, 클라이언트로부터 웹 요청을 받아 선택한 서버로 전달한다. 라우팅은 sandbox와 서비스를 선택한다. 권한 확인은 요청자가 해당 sandbox와 서비스에 접근할 수 있는지 검사한다. gateway에서 그 결정을 적용하려면 접근 권한을 확인하는 이 경로로만 서비스에 도달할 수 있게 해야 한다.

경로가 무엇을 노출하고 언제 닫히는지 확인한다. 미리보기 경로는 sandbox의 다른 서비스를 노출할 필요가 없으며, 세션이 끝나면 닫혀야 한다. 외부 클라이언트가 연결을 시작했더라도 미리보기 서버의 응답은 [egress](egress.md) 트래픽으로 sandbox를 빠져나간다.

[용어집으로 돌아가기](../glossary.md)
