# Capability

이 책에서 capability는 코드를 실행하는 시스템이 접근을 허용해 코드가 사용할 수 있게 된 리소스나 작업을 뜻한다. 무엇을 허용했는지 이해하려면 코드가 어떤 작업을 할 수 있는지와 그 작업을 어떤 대상에 수행할 수 있는지를 모두 확인한다. 좁은 범위의 권한을 부여해도 코드가 다른 방식으로 얻은 더 넓은 접근 권한은 사라지지 않는다.

## 예시

보고용 script는 특정 프로젝트의 issue 제목을 반환하는 [tool](tool.md) 하나를 갖춘 [sandbox](sandbox.md)에서 실행된다. script는 해당 제목을 읽을 수 있지만, issue를 수정하거나 임의의 네트워크 요청을 보낼 수는 없다. 호출을 처리하는 서비스는 자체 [credential](credential.md)을 사용하며, 이를 script에 넘기지 않는다.

## 권한을 부여하는 범위

[host function](host-function.md)은 issue 조회 같은 작업을 허용할 수 있다. 읽기 전용 [mount](mount.md)는 파일에 접근할 수 있게 하되, 그 mount를 통해 파일을 변경하는 것은 허용하지 않을 수 있다. 두 경우 모두 workload 외부의 구성 요소가 제한을 적용한다. tool handler가 요청 대상 issue를 확인하거나, 운영 체제가 읽기 전용 접근을 적용한다.

capability는 이름이 아니라 실제 효과를 기준으로 판단한다. 이름이 “read issue”인 tool도 handler가 요청 대상 프로젝트를 확인할 때만 접근 범위가 해당 프로젝트로 제한된다. 일반적인 네트워크 접근 권한과 API token이 있는 script는 그 tool 없이도 작업을 수행할 수 있으므로, [least privilege](least-privilege.md)를 적용할 때는 직접 접근과 tool을 통한 접근을 모두 평가한다.

[용어집으로 돌아가기](index.md)
