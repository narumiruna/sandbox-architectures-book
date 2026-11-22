# Observability와 디버깅 {#observability-and-debugging}

마지막으로 성공한 단계부터 확인합니다. worker가 준비되지 않은 경우, 접근 규칙이 동작을 차단한 경우, 컴파일러가 실행됐지만 오류를 반환한 경우에는 각각 다른 조치가 필요합니다. [Observability](../../glossary/observability.md)란 이런 경우를 구분할 만큼 충분한 증거를 확보할 수 있는 것을 뜻합니다. `failed` 같은 상태 하나만으로는 충분하지 않습니다.

[Lamp 예제](../design/from-issue-to-patch.md)를 사용해 이슈 조회, worker 설정, 빌드, 정리까지 한 번의 실행을 추적합니다.

## 증거를 담당 계층과 연결하기 {#match-the-evidence-to-the-layer}

[Control plane](../../glossary/control-plane.md)은 실행이 요청된 시각, worker가 준비된 시각, 실행이 중지된 시각을 기록하고 정리 상태는 별도로 기록합니다. [Runtime](../../glossary/runtime.md)은 명령 실행 결과와 실행 한도 관련 이벤트를 보고합니다. Tool handler는 이슈 접근 허용 여부를 기록하고, 수집기는 내보내기 성공 여부를 기록합니다. 비밀이 아닌 요청 ID와 시도 ID로 이 기록을 연결합니다. 사건의 순서를 파악할 수 있도록 UTC 타임스탬프를 기록하고, 소요 시간은 시각이 갑자기 바뀌지 않는 시계로 재서 기록합니다.

아래는 서로 별개인 세 가지 가상 시도입니다. 타임스탬프와 로그 발췌는 증거를 읽는 방법만을 보여 줍니다.

| 시도와 UTC 기준 상태 | 민감 정보를 가린 증거 | 담당 계층과 다음 확인 사항 |
| --- | --- | --- |
| A1: `10:00:00 provisioning` → `10:00:30 timed_out` | `workspace_attach_timeout`이 기록됐으며 `ready` 이벤트는 없습니다. | Control plane과 workspace 서비스: 승인된 사본을 연결하지 못한 이유를 확인합니다. 일부만 할당된 자원이 정리됐는지도 확인합니다. |
| A2: `10:01:00 lookup` → `10:01:01 access_denied` | 이슈 handler는 Lamp의 범위를 벗어난 가상 요청을 거부하고 이슈 기록을 읽지 않습니다. | 이슈 handler 담당자: 실행에 부여된 범위를 확인합니다. 검사를 통과시키려고 규칙을 완화하지 않습니다. |
| A3: `10:02:00 ready` → `10:02:02 build_failed` | `compile_failed`가 기록됐으며 종료 상태는 `1`입니다. 테스트는 실행되지 않았습니다. | 요청자는 승인된 사본에서 빌드를 재현해 오류를 진단할 수 있습니다. 패치 초안이나 컴파일러 원본 로그는 보관하지 않습니다. |

접근 거부는 개별 이벤트이며 반드시 session의 최종 결과인 것은 아닙니다. 이후에 발생한 실패의 원인을 접근 거부로 판단하기 전에 어느 명령이 다음에 실행됐는지 확인합니다. [Resource limit](resource-limits.md)이 원인일 수 있다면 종료 코드로 추측하지 말고, 한도를 적용하는 계층이 명시적으로 한도 관련 이벤트를 남겼는지 확인합니다.

## 진단 기록을 안전하게 보관하기 {#keep-diagnostic-records-safe}

실행 ID와 시도 ID, 타임스탬프, 단계, 상태, 사유 코드처럼 안전한 메타데이터만 보관합니다. 환경 덤프, 가공하지 않은 인수, 이슈 본문, [credential](../../glossary/credential.md) 값, workspace의 내용은 로그에 남기지 않습니다. 해당 tenant를 담당하는 운영자만 접근할 수 있습니다. 서비스 운영자는 제거를 확인할 때까지 정리 기록을 보관하고, 그 뒤 해당 시도의 진단 기록을 30일 후에 만료시킵니다. `cleaned_up` 이벤트는 worker가 정리됐음을 확인해 줄 뿐, 검토를 위해 받아들인 파일이나 진단 기록까지 삭제됐다는 뜻은 아닙니다.

[결정 기록](../design/from-issue-to-patch.md#fill-in-your-decision-record)으로 돌아가 각 사본의 담당자와 만료 시점을 적습니다. 그런 다음 [접근 규칙 검증](../verification/verifying-access-rules.md)에 따라 허용된 동작이 성공하고 금지된 동작이 예상한 이유로 실패하는지 테스트합니다.
