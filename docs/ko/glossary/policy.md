# Policy

Policy는 실행 중인 코드가 어떤 작업을 할 수 있고 어떤 리소스를 사용할 수 있는지 정하는 규칙의 집합이다. 규칙은 신뢰할 수 있는 구성 요소가 적용해야만 효력이 있다. 모델에 내리는 지시 자체는 접근 제한이 아니다.

## 예시

Lamp의 테스트 [sandbox](sandbox.md)는 `total.c`를 읽고 임시 출력을 쓸 수 있지만, [host](host.md)의 SSH 키는 열 수 없다. [process sandbox](operating-system-process-sandbox.md)의 설정은 프로젝트 파일을 읽기 전용으로 지정하고 임시 디렉터리에는 쓰기를 허용한다. Host [kernel](kernel.md)은 각 파일 요청을 이 설정에 비추어 검사한다. Runner에서는 해당 키가 보이지 않는다.

## 각 규칙을 집행할 구성 요소 지정하기

[control plane](control-plane.md)은 sandbox를 생성할 때 policy를 선택할 수 있다. [runtime](runtime.md), 운영 체제, proxy 또는 [tool](tool.md) handler는 각각 자신이 관찰할 수 있는 부분을 집행한다. 예를 들어 [Linux kernel 문서](https://docs.kernel.org/userspace-api/seccomp_filter.html)에 따르면 [seccomp](seccomp.md)는 kernel로 보내는 요청을 필터링할 수 있지만, 요청이 파일 이름의 메모리 위치만 전달하면 필터는 파일 이름을 읽을 수 없다. 파일에 직접 접근하는 경우에는 filesystem 제어 기능을 사용해 파일 경로에 관한 규칙을 집행한다.

## 언제 중요한가

Sandbox를 구성하거나 테스트할 때는 각 [isolation boundary](isolation-boundary.md)에서 어떤 작업이 성공해야 하고 어떤 작업이 실패해야 하는지 확인한다. 같은 리소스에 [mount](mount.md)와 tool 양쪽으로 접근할 수 있다면 두 경로를 모두 확인한다. 한 경로에서 접근을 거부해도 다른 경로에서까지 거부되는 것은 아니다. 파일 규칙을 이루는 두 부분은 [파일을 여는 요청 따라가기](../sandbox-isolation-boundaries.md#follow-a-request-to-open-a-file)를 참고한다.

[Glossary로 돌아가기](index.md)
