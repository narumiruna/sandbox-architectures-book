# Least privilege

Least privilege는 코드에 작업에 필요한 권한만 주는 것을 뜻한다. 코드가 할 수 있는 동작과 그 대상, 접근할 수 있는 기간을 필요한 범위로 제한한다. 판단 기준은 설정에 적힌 내용이 아니라 코드가 실제로 무엇에 접근할 수 있는지다. 여기에는 tool을 통한 접근도 포함된다.

## 예시

의존성 보고서를 만들려면 프로젝트의 패키지 manifest를 읽고 버전 정보를 조회해야 한다. 이 작업의 [sandbox](sandbox.md)는 manifest의 읽기 전용 복사본과 승인된 registry에 대한 버전 조회 [tool](tool.md)을 제공한다. 이 작업에는 작업 공간에 대한 쓰기 권한, 제한 없는 네트워크 연결, 작업 자체에 발급된 registry token이 필요하지 않다.

## 권한을 부여할 때마다 범위 좁히기

먼저 [workload](workload.md)에 필요한 동작을 확인한다. 파일 접근은 필요한 파일로 한정하고 읽기와 쓰기 권한을 분리한다. 특정 tool 동작만으로 충분하면 범용 인터페이스보다 그 동작을 우선한다. 서비스가 요청을 인증해야 한다면 코드에 재사용 가능한 비밀 값을 넘겨주는 대신 승인된 요청에 [credential injection](credential-injection.md)을 적용할 수 있다. 작업이 끝나면 임시 접근 권한을 종료한다.

허용된 접근 경로를 하나씩 확인한다. 읽기 전용 [mount](mount.md)는 그 mount를 통한 쓰기를 막지만, 별도의 tool이 같은 파일에 쓰는 것까지 막지는 않는다. Tool handler가 자체 제한을 적용해야 한다. Least privilege는 workload가 영향을 줄 수 있는 범위를 줄이지만, workload에 허용된 동작에서 피해가 발생하는 것까지 막지는 못한다.

[용어집으로 돌아가기](index.md)
