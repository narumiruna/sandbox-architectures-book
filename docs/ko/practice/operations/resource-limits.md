# Resource limit {#resource-limits}

[Resource limit](../../glossary/resource-limit.md)은 worker가 자원을 얼마나 쓸 수 있는지 정합니다. 접근 규칙은 worker가 무엇에 접근할 수 있는지 정합니다. 디스크 한도를 두면 빌드가 저장 공간을 가득 채우는 일을 막을 수 있지만, worker가 다른 프로젝트의 파일에 접근하는 일을 막으려면 접근 규칙이 필요합니다.

[Lamp 예제](../design/from-issue-to-patch.md)에서는 worker에 주는 자원 예산으로 빌드 파일 작성뿐 아니라 C 프로그램의 컴파일과 테스트까지 할 수 있어야 합니다.

## 자원 예산과 한도에 도달했을 때의 동작 정하기 {#set-a-budget-and-decide-what-happens-at-the-limit}

아래 한도는 예시일 뿐, 기본값이나 측정으로 확인한 요구량이 아닙니다. 첫 명령만이 아니라 컴파일러와 테스트 process를 포함한 worker 전체의 사용량을 합산합니다. [Control plane](../../glossary/control-plane.md)은 자원 예산을 정하고, 작업 요청을 받아들일지 판단하며, 기한을 적용합니다. [Runtime](../../glossary/runtime.md)은 실행에 쓰는 자원에 상한을 두고, workspace 서비스는 임시 저장 공간을 제한합니다.

| 제한 항목 | 자원 예산 예시 | 한도에 도달했을 때의 동작 |
| --- | --- | --- |
| CPU | 사용량을 집계하는 각 구간마다 CPU 하나가 제공할 수 있는 실행 시간 이내로 제한합니다. | Runtime은 worker를 중지하지 않고 실행 속도를 늦춥니다. 이 상한은 Lamp에 CPU 하나를 예약해 주는 것이 아닙니다. |
| 메모리 | Linux와 worker의 모든 process가 VM 메모리 256 MiB를 공유합니다. | Runtime이 메모리 한도로 인한 실패를 보고하면 실행을 중지합니다. 아무것도 바꾸지 않은 채 다시 시도하지 않습니다. |
| 디스크 | 미리 준비한 입력과 임시 빌드 파일을 포함하여, 쓰기 가능한 `/work` 디스크 전체에 64 MiB를 배정합니다. | 예산을 넘는 쓰기는 실패합니다. 디스크 한도 때문에 빌드가 실패하면 안전한 사유 코드를 반환하고 미완성 파일은 버립니다. |
| 시간 | 큐 대기, worker 시작, 명령 실행에 각각 30초를 배정하고, 단계별로 따로 시간을 잽니다. | 기한이 되면 대기 중인 요청을 만료시키거나 이미 시작한 시도를 중지합니다. 어느 단계에서 시간이 초과되었는지 기록합니다. |
| 수용량 | [Tenant](../../glossary/tenant.md)당 worker 하나만 할당합니다. 준비 중이거나 정리 중인 worker도 포함하며, tenant마다 요청을 최대 두 건 더 대기시킬 수 있습니다. | 자리가 남을 때만 요청을 큐에 넣습니다. 한도를 넘는 요청은 거부합니다. 첫 번째 Lamp worker가 아직 할당 자리를 차지하고 있으면 두 번째 worker를 시작하지 않습니다. |

## 미완성 출력을 성공으로 판단하지 않기 {#do-not-mistake-partial-output-for-success}

Lamp가 링크 단계에서 디스크 한도에 도달하면, 미완성 binary가 남고 테스트는 시작조차 못 할 수 있습니다. 시도가 실패하거나 취소되거나 시간을 초과하면, 미완성 패치나 원본 로그 또는 binary 대신 상태와 안전한 사유 코드를 반환합니다. 한도를 적용하는 계층에서 보고한 경우에만 어떤 한도 때문에 실패했는지 기록합니다. Control plane은 worker를 중지하고 성공했을 때와 동일한 [정리 규칙](sandbox-lifecycle.md#what-gets-deleted-and-when)을 따릅니다. 권한이 있는 요청자는 원인을 해결한 뒤 새로 시도할 수 있습니다. 같은 예산으로 자동 재시도하면 같은 실패가 반복될 수 있습니다.

수집기는 별도로 [출력 크기 제한](../data-and-access/workspaces-and-artifacts.md#decide-what-leaves-work)을 적용합니다. 빌드와 테스트는 통과했더라도 내보내기가 실패할 수 있습니다. 이때도 두 결과물이 모두 준비되지 않으면 어느 것도 공개하지 않습니다.

다음: [Observability와 디버깅](observability-and-debugging.md)에서는 한도에 도달한 사건을 접근 거부나 빌드 실패와 구분하는 방법을 설명합니다.
