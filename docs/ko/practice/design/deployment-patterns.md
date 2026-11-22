# 배포 패턴 {#deployment-patterns}

[sandbox가 무엇을 격리하는지](choosing-a-sandbox.md)와 별개로 worker를 어디에서 실행하고 누가 운영할지 결정합니다. 원격 인프라의 worker는 직접 운영할 수도 있고 제공자가 운영할 수도 있습니다. 네 가지 구성 모두 같은 읽기 전용 [tool](../../glossary/tool.md)로 Lamp의 이슈 `LAMP-17`을 가져오고, 별도의 Linux worker에서 작은 C 프로그램의 잘못된 합계를 고칩니다. Worker는 복사본을 컴파일하고 테스트한 뒤, 검토할 수 있도록 텍스트 패치와 테스트 출력을 반환합니다. Worker는 결과를 게시할 수 없습니다.

## 모든 구성에 공통인 사항 {#what-stays-the-same}

Linux worker에는 원본 저장소의 쓰기 가능한 [mount](../../glossary/mount.md) 대신 쓰고 버리는 [workspace](../../glossary/workspace.md)를 제공합니다. 이슈 tool은 가상의 테스트 데이터를 읽으며 서비스 [credential](../../glossary/credential.md)을 사용하지 않습니다. 이슈 읽기용 credential이 필요하다면 아래에 나오는 각 담당자가 스크립트와 worker 양쪽의 외부에서 보관합니다. 게시 권한은 이 작업 흐름 밖의 별도 역할에만 부여합니다. 패치와 로그는 검토자만 접근할 수 있고 만료 시점이 명시된 [artifact](../../glossary/artifact.md)로 보관합니다.

## 각 구성은 누가 운영합니까? {#who-operates-each-layout}

### 로컬 워크스테이션 {#local-workstation}

개발자는 스크립트 runtime과 Linux runtime을 모두 운영하며 이슈 tool과 읽기용 credential이 있다면 그 credential도 관리합니다. 로컬 컨트롤러가 임시 복사본을 만들고, 실행이 끝나면 worker를 중지하고 복사본을 삭제합니다. 개발자는 검토 디렉터리에 대한 접근을 제한하고 검토 기간이 끝나면 저장된 출력을 삭제합니다. 이 구성에서는 작업 흐름 전체가 개발자의 컴퓨터에서 진행되지만, runtime은 여전히 worker가 개발자의 홈 디렉터리와 원본 체크아웃에 접근하지 못하게 해야 합니다.

### 지속적 통합(CI) {#continuous-integration-ci}

[Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration)(CI)은 실행을 자동으로 시작할 수 있지만 격리 수단은 아닙니다. 이 구성에서는 runner 운영자가 두 [runtime](../../glossary/runtime.md)을 유지 관리합니다. 프로젝트 팀은 소스 revision을 선택하고 이슈 tool과 읽기용 credential이 있다면 그 credential도 관리하며, 누가 언제까지 artifact를 읽을 수 있는지 정합니다. CI 작업 컨트롤러는 임시 복사본을 준비하고, 작업이 실패한 경우에도 이를 삭제합니다. CI artifact 저장소는 프로젝트가 정한 일정에 따라 저장된 출력을 만료시킵니다. 작업은 프로젝트의 기존 검토 절차를 이용하면서도 그 절차의 릴리스 권한을 물려받지 않을 수 있습니다.

### 자체 운영 서비스 {#self-hosted-service}

내부 플랫폼 팀은 사내에 있든 클라우드에 있든 직접 운영하는 인프라에서 두 runtime을 모두 운영하고 실행마다 임시 저장 공간을 제공합니다. 각 프로젝트 팀은 소스, 이슈 tool과 그 읽기 권한, 검토 접근 [policy](../../glossary/policy.md)를 관리합니다. 플랫폼 팀의 [control plane](../../glossary/control-plane.md)은 실패했거나 기한이 만료된 worker를 중지하고 임시 저장 공간을 제거하며 프로젝트 policy에 따라 보관된 출력을 만료시킵니다. 플랫폼 팀은 runtime에 패치를 적용하고 가용 용량을 모니터링하며 장애에도 대응해야 합니다.

### 관리형 worker 서비스 {#managed-worker-service}

고객은 스크립트 runtime을 운영하고 이슈 tool과 읽기용 credential이 있다면 그 credential도 관리합니다. 제공자는 Linux runtime을 운영하고 worker의 임시 저장 공간을 만들고 제거합니다. 고객은 사용할 소스 복사본을 선택하고 자체 검토 저장소의 접근과 만료를 제어합니다. 고객은 작업을 취소한 경우를 포함해 제공자가 무엇을 삭제하고 무엇을 보관하는지도 확인해야 합니다. 작업이 종료되어도 로그, cache, [snapshot](../../glossary/snapshot.md)과 같은 별도 사본까지 삭제되는 것은 아닙니다.

## 세 가지를 따로 결정하기 {#make-three-separate-decisions}

1. **배치:** 승인된 파일을 워크스테이션이나 조직 밖으로 내보내도 됩니까? 작업이 실행되는 곳과 작업의 상태 및 출력이 저장되는 곳을 기록합니다.
2. **운영 책임:** 누가 runtime에 패치를 적용하고, 실패한 작업을 처리하고, 정리가 제대로 됐는지 확인하고, 용량 비용을 부담합니까? 자체 운영 서비스에 드는 인력 시간과 인프라 비용을, 관리형 서비스의 이용료와 고객이 여전히 맡아야 하는 업무에 견주어 비교합니다.
3. **실행 경계:** 로컬 worker도 [virtual machine (VM)](../../glossary/virtual-machine.md)을 사용할 수 있고, 원격 worker도 [host](../../glossary/host.md) [kernel](../../glossary/kernel.md)을 공유할 수 있습니다. 어느 runtime이 [isolation boundary](../../glossary/isolation-boundary.md)를 적용하는지, 어떤 작업이 그 경계를 공유하는지, 무엇이 경계를 넘을 수 있는지 확인합니다. 구현 예시는 [아키텍처 조사](../../agent-sandbox-architectures.md)를 참고하세요.

다음: 스크립트가 sandbox 안에서 실행될 때도 이슈 조회 tool이 무엇을 확인해야 하는지 [Tool 호출 권한 확인](tool-authorization.md)에서 살펴보고 접근 규칙을 정하기 시작합니다.
