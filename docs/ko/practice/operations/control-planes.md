# Control plane {#control-planes}

[control plane](../../glossary/control-plane.md)은 [sandbox](../../glossary/sandbox.md)를 어디서 실행할지, 무엇을 제공할지, 언제 제거할지 결정합니다. [runtime](../../glossary/runtime.md)은 [isolation boundary](../../glossary/isolation-boundary.md) 안에서 코드 실행을 준비하고 코드를 실행합니다. 경계가 아무리 강해도 control plane이 프로젝트 파일을 잘못된 실행에 연결하면 그 프로젝트를 보호할 수 없습니다.

[Lamp 예제](../design/from-issue-to-patch.md)에서 control plane은 소스 사본을 빌드하고 테스트할 별도의 Linux worker를 준비한 뒤 worker와 사본을 제거합니다.

## 요청부터 정리까지 {#from-request-to-cleanup}

1. **권한을 확인하고 policy를 선택합니다.** Control plane은 요청자가 `LAMP-17`을 위한 Lamp [session](../../glossary/sandbox-session.md)을 시작하고 요청한 소스 리비전을 사용할 권한이 있는지 확인합니다. 그런 다음 이 입력을 해당 실행에 연결합니다. Control plane의 [policy](../../glossary/policy.md)는 runtime, workspace 서비스, 수집기가 지켜야 할 요구 사항을 정합니다. 각 구성 요소는 그 요구 사항을 실제로 적용합니다. 이슈 tool은 여전히 자체 레코드의 접근 권한을 확인합니다.
2. **Worker를 배치하고 준비합니다.** Control plane은 여유 자원이 있는 [host](../../glossary/host.md)를 선택합니다. 이 host는 새 [virtual machine (VM)](../../glossary/virtual-machine.md)을 실행할 수 있어야 합니다. Workspace 서비스에는 승인된 Lamp 사본을, runtime에는 VM을 요청합니다. 첫 명령을 허용하기 전에 보고받은 구성을 확인합니다. 올바른 workspace, 깨끗한 image, 자원 한도가 설정되어 있어야 하며 외부 네트워크에 연결되어 있으면 안 됩니다. 요구 사항을 충족할 수 없으면 대기열의 제한 시간 안에서 기다리거나 해당 시도를 실패 처리하세요. 더 약한 구성으로 바꾸지 마세요.
3. **실행하고 중지한 뒤 결과를 수집합니다.** VM은 실행 중인 코드가 노출된 자원에만 접근할 수 있게 제한합니다. Runtime이 명령 상태를 보고하면 control plane이 worker를 중지합니다. 빌드와 테스트가 모두 성공적으로 끝난 뒤에만 수집기는 지정된 두 텍스트 파일을 수락할 수 있습니다. 검토 저장소는 검토자의 접근 권한을 별도로 확인합니다.
4. **정리가 끝났는지 확인합니다.** Control plane은 설정이 일부만 끝났거나 내보내기가 실패한 경우를 포함해, 모든 종료 경로에서 자원이 제거되는지 추적합니다. 제거가 확인되지 않으면 자원을 사용하지 못하게 하고 정리를 다시 시도한 뒤 운영자에게 알리세요. 수락한 [artifact](../../glossary/artifact.md)의 보관 기간 만료는 검토 저장소가 관리합니다. Worker를 정리해도 이 보관 기간은 끝나지 않습니다.

## 구성 요소별 책임 {#who-owns-what}

| 구성 요소 | 이 예제에서의 책임 |
| --- | --- |
| Control plane | 각 실행을 해당 [tenant](../../glossary/tenant.md), 이슈, 리비전에 연결합니다. 구성을 선택하고 준비 상태, 제한 시간, 정리 상태를 추적합니다. |
| Interpreter와 VM runtime | Interpreter는 스크립트가 호출할 수 있는 동작을 제한합니다. VM runtime은 설정된 자원만 노출하고 worker의 상태와 제거 여부를 보고합니다. |
| 이슈 tool 처리기 | `LAMP-17`의 접근 권한을 확인하고 허용된 필드만 반환합니다. |
| Workspace 서비스 | 해당 실행의 디스크에 승인된 Lamp 사본을 제공하고, 디스크 용량 한도를 적용하며, 디스크가 제거되었는지 확인합니다. |
| 수집기 | 해당 실행의 디스크에 있는 두 파일을 검증하고 일치하는 검토 항목에 저장합니다. |
| 검토 저장소 | 검토자가 읽을 때마다 권한을 확인하고, 보관 기간이 만료되면 수락한 파일을 삭제합니다. |
| 서비스 운영자 | 환경 준비 실패, 자원 용량 문제, 정리 실패를 조사합니다. Worker의 작업용 임시 파일이 아니라 진단 레코드를 사용합니다. |

이 호스팅 예제에서는 플랫폼 팀이 control plane, runtime, 저장소 서비스를 운영합니다. Lamp 프로젝트 소유자는 예제용 이슈 데이터를 제공하고 어느 호출자가 Lamp 작업을 실행하고 검토할 수 있는지 결정합니다. 다른 주체가 worker를 운영할 때 책임이 어떻게 달라지는지는 [배포 패턴](../design/deployment-patterns.md)을 참고하세요.

다음: [Sandbox 수명 주기](sandbox-lifecycle.md)에서는 단계가 바뀔 때마다 서비스가 무엇을 보관하고 삭제하는지 살펴봅니다.
