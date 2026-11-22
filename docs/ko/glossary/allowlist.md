# Allowlist

allowlist는 프로그램이 사용할 수 있는 리소스나 수행할 수 있는 작업을 명시한다. 신뢰할 수 있는 구성 요소가 요청을 검사하고 목록과 일치하지 않는 요청을 차단할 때만 접근이 제한된다.

## 예시

빌드 sandbox에서 소프트웨어 패키지를 다운로드해야 한다. 이 sandbox의 [policy](policy.md)는 해당 패키지의 복사본을 저장하는 팀의 패키지 미러 서버로만 [egress](egress.md) 연결을 허용한다. 새 연결을 하나씩 검사하는 네트워크 제어 구성 요소가 목록을 적용한다. 목록 자체는 트래픽을 차단하지 않는다.

## 규칙이 검사할 수 있는 항목

검사 범위는 검사를 수행하는 구성 요소가 무엇을 볼 수 있는지에 따라 달라진다. 연결 규칙은 목적지와 포트가 일치하는지 확인할 수 있다. 웹 요청을 전달하고 내용을 읽는 서비스는 요청의 작업과 경로도 검사할 수 있다. [OpenShell v0.1.9 네트워크 규칙](https://github.com/NVIDIA/OpenShell/blob/v0.1.9/docs/how-it-works/policies/network-rules.mdx#connection-and-request-checks)은 이 두 수준의 검사를 보여 준다.

서비스로의 연결을 허용하는 것만으로는 workload가 서비스에 보낼 수 있는 내용이나 서비스가 받아들이는 작업을 제한할 수 없다. workload에 작업 하나만 필요하다면 [least privilege](least-privilege.md)를 적용하기 위해 목적지뿐 아니라 작업도 일치하는지 확인한다. 제한하려는 접근이 규칙을 적용하는 구성 요소를 반드시 거치게 한다. 한 경로에서 수행하는 검사는 다른 경로에 적용되지 않는다.

[용어집으로 돌아가기](index.md)
