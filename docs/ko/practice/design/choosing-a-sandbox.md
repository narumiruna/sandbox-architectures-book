# Sandbox 고르기 {#choosing-a-sandbox}

코드가 해야 할 일과 접근하면 안 되는 대상을 기준으로 [sandbox](../../glossary/sandbox.md)를 고릅니다. 서비스 규모만으로는 얼마나 강한 경계가 필요한지 알 수 없습니다. 개인 프로젝트도 신뢰할 수 없는 코드를 실행할 수 있고, 대규모 서비스에도 이슈를 읽기만 하는 작업이 있을 수 있습니다.

## 요구 사항에서 결정 기록까지 {#from-requirements-to-a-decision-record}

다음 절차를 [Lamp 결정 기록 양식](from-issue-to-patch.md#fill-in-your-decision-record)과 함께 사용합니다.

1. **가능해야 할 일과 접근을 막아야 할 대상을 나열합니다.** 소스, 테스트, 빌드 지침, [agent](../../glossary/agent.md)가 생성한 명령 등 [workload](../../glossary/workload.md)를 누가 제공하거나 변경할 수 있는지 기록합니다. 필요한 파일, 동작, 연결을 나열합니다. 작업이 [host](../../glossary/host.md) 운영체제의 핵심인 [kernel](../../glossary/kernel.md)을 사용해도 되는지, 다른 작업과 kernel을 공유해도 되는지 결정합니다.
2. **제품을 고르기 전에 [isolation boundary](../../glossary/isolation-boundary.md)를 선택합니다.** [Restricted interpreter](../../glossary/restricted-interpreter.md)는 스크립트에 읽기 전용 [tool](../../glossary/tool.md) 하나를 사용할 수 있게 해 줍니다. 그래도 tool은 요청마다 [authorization](../../glossary/authorization.md)을 확인합니다. Worker가 컴파일러와 자식 process를 실행해야 하지만 host kernel은 사용하면 안 된다면 [operating-system process sandbox](../../glossary/operating-system-process-sandbox.md)는 요구 사항을 충족하지 못합니다. Worker에 자체 Linux kernel이 필요하다면 [virtual machine (VM)](../../glossary/virtual-machine.md)을 평가합니다. [어디에서 실행하고 누가 운영할지](deployment-patterns.md)는 별도로 결정합니다.
3. **어떤 작업이 한 환경을 공유할지, 즉 [isolation unit](../../glossary/isolation-unit.md)을 정합니다.** 예를 들어 작업마다 새 VM을 쓰는 방식과 한 고객이 VM을 재사용하는 방식은 경계의 종류는 같지만 공유 규칙은 다릅니다. 무엇을 남겨도 되는지, 무엇을 제거해야 하는지, 성공·실패·취소 후 정리를 누가 검증하는지 기록합니다.
4. **비용이나 속도를 비교하기 전에 요구 사항을 테스트합니다.** 같은 소스 revision, 테스트, toolchain을 사용합니다. 허용된 동작은 성공하고 금지된 동작은 의도한 이유로 실패하는지 확인합니다. 요구 사항을 충족하는 후보만 비교합니다. 대기 시간과 설정 시간을 포함해 제출부터 검토 가능한 출력이 나오기까지 걸리는 시간을 측정합니다. CPU, 메모리, 디스크 사용량과 cache 상태, 작업당 운영 비용이 있다면 그 비용도 기록합니다. 테스트하기 전에 목표를 정합니다. 모든 요구 사항에 대해 충족 여부가 **문서에 명시됨**, **측정됨**, **확인되지 않음** 중 어디에 해당하는지 표시합니다. 확인되지 않은 요구 사항은 통과로 보지 않습니다. [후보 평가](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)와 [Sandbox 측정](../verification/measuring-a-sandbox.md)을 참고하세요.

## 같은 Lamp 작업에 대한 세 가지 결정 {#three-decisions-for-the-same-lamp-task}

세 환경 모두에서 [Lamp 작업](from-issue-to-patch.md)은 `LAMP-17`을 읽고, 작은 C 프로그램의 잘못된 합계를 수정하고, 수정한 코드를 컴파일한 뒤 항목 두 개에 세 개를 더하면 다섯 개가 되는지 테스트합니다. 조회 스크립트는 restricted interpreter에서 읽기 전용 이슈 tool만 사용합니다. 별도의 Linux worker는 revision이 확인된 일회용 [workspace](../../glossary/workspace.md)를 수정합니다. Worker에는 네트워크 접근, 이슈 tool, 저장소 [credential](../../glossary/credential.md)이 필요하지 않습니다. 검토용 [artifact](../../glossary/artifact.md)는 `change.patch`와 `test.log`뿐입니다. 권한이 있는 검토자만 읽을 수 있으며 7일 후 만료됩니다. Worker는 결과를 게시할 수 없습니다. 아래 기록은 설계 제안이며 테스트 결과가 아닙니다.

### Linux 워크스테이션에서 진행하는 개인 프로젝트 {#personal-project-on-a-linux-workstation}

- **요구 사항:** 개발자가 실행을 시작하지만 agent의 명령은 신뢰하지 않습니다. Worker와 그 자식 process는 개발자의 홈 디렉터리나 credential을 읽거나 원본 체크아웃을 변경할 수 없어야 합니다. 이 프로젝트에서는 워크스테이션의 kernel을 공유해도 됩니다.
- **경계와 단위:** Operating-system process sandbox에서 native tool을 실행합니다. 빌드와 테스트는 이번 실행에 한해서만 sandbox 하나를 공유합니다.
- **보관과 정리:** 설치되어 있는 읽기 전용 toolchain은 재사용하지만 worker나 이전 빌드 디렉터리는 재사용하지 않습니다. Process 트리 전체를 중지하고 임시 복사본과 빌드 파일을 제거합니다. 두 출력은 만료될 때까지 개발자가 사용하는 접근 제한 검토 디렉터리에 보관합니다.
- **이 방식을 택한 이유:** 일반 셸은 이런 파일 접근 제한을 제공하지 않습니다. 별도의 guest kernel을 두면 이 프로젝트에 필요하지 않은 설정 작업이 늘어납니다.
- **다시 검토할 때:** 외부 기여자가 빌드나 테스트를 제공할 수 있게 되거나 워크스테이션이 더 이상 worker와 kernel을 공유할 수 없을 때입니다.

### 회사 내 여러 팀이 사용하는 내부 서비스 {#internal-service-for-several-company-teams}

- **요구 사항:** 팀 구성원이 빌드와 테스트를 변경할 수 있습니다. Worker는 host 또는 다른 작업과 kernel을 공유하면 안 됩니다. 이슈 읽기, workspace 연결, artifact 읽기 전에 호출자의 팀과 프로젝트를 확인합니다. 작업을 시작한 사람, 프로젝트와 revision, 결과를 기록합니다. 실패한 실행의 처리와 정리는 플랫폼 팀이 맡습니다.
- **경계와 단위:** 내부 runner에서 실행마다 새 Linux VM을 시작합니다. 같은 팀의 연속 실행도 guest를 공유하지 않습니다.
- **보관과 정리:** 컴파일러는 있지만 팀 데이터는 없는 읽기 전용 base image를 재사용합니다. Guest를 폐기하고 그 임시 저장 공간과 빌드 파일을 제거합니다. 감사 기록과 해당 팀 범위로 제한된 두 출력은 각각의 보존 규칙에 따라 보관합니다.
- **이 방식을 택한 이유:** Host kernel을 사용하는 process sandbox는 별도 kernel 규칙을 충족하지 못합니다. 팀이 VM을 재사용하려면 실행 사이에 초기화가 제대로 이루어졌는지 검증해야 합니다. 실패한 작업이 남긴 파일이 재시도에 넘어가지 않도록 처음에는 재사용하지 않습니다.
- **다시 검토할 때:** 내부 API가 필요해지거나, 직원이 아닌 사람이 제공한 코드를 받기 시작하거나, 대기 시간 목표를 달성하지 못할 때입니다. 접근 제어가 빠진 것이 문제인지, 단순히 worker가 부족한 것인지 확인합니다.

### 서로 관련 없는 고객이 사용하는 대규모 서비스 {#large-service-for-unrelated-customers}

- **요구 사항:** 등록된 고객은 누구나 코드를 제공할 수 있습니다. [Tenant](../../glossary/tenant.md)는 데이터와 작업을 다른 고객과 분리해야 하는 고객입니다. 어느 작업도 host나 다른 작업과 kernel을 공유하지 않습니다. 이슈 조회, workspace 연결, artifact 가져오기 각각에 tenant별 접근 규칙을 적용합니다. [Resource limit](../../glossary/resource-limit.md)과 tenant별 동시 실행 상한을 적용합니다. 상한을 넘는 작업은 기다리거나 거부되지만 다른 tenant는 여유 용량이 있으면 작업을 시작할 수 있습니다.
- **경계와 단위:** 작업마다 새 Linux VM을 시작하고 하나의 tenant에 할당합니다. Policy에서 허용할 때만 runner 하드웨어를 공유하며, 고객 작업 간에는 guest를 공유하지 않습니다.
- **보관과 정리:** 고객 데이터가 없는 읽기 전용 base image를 재사용합니다. 실행 중인 guest나 고객 cache는 재사용하지 않습니다. 취소한 경우에도 guest와 임시 저장 공간을 폐기합니다. 패치와 테스트 출력은 만료될 때까지 해당 tenant 범위로 제한된 검토 저장소에 보관합니다. 재시도에는 새 저장 공간을 사용합니다.
- **이 방식을 택한 이유:** Host kernel을 사용하는 process sandbox도, 공유 guest도 kernel 규칙을 충족하지 못합니다. Tenant마다 VM을 하나씩 두면 guest 경계에서 tenant를 분리할 수 있지만, 같은 tenant의 작업끼리는 여전히 서로의 상태에 영향을 줄 수 있습니다. 별도 VM을 사용해도 잘못 설정된 이슈 tool이나 저장소 서비스의 문제는 해결되지 않습니다.
- **다시 검토할 때:** 부하가 가장 높을 때 대기 시간, 완료율, 작업당 비용 중 하나라도 목표를 벗어날 때입니다. Runner 슬롯 부족이 병목이라면 용량을 늘립니다. Host 공유에 대한 전제가 바뀌면 경계나 배치를 다시 검토합니다. 재사용을 허용하기 전에 후속 작업에서 무엇을 볼 수 있는지 확인합니다.

허용해야 할 경로와 차단해야 할 경로는 [무해한 접근 검사](../verification/verifying-access-rules.md)로 테스트하고, 공유 서비스에는 [tenant 격리 검사](../data-and-access/multi-tenant-isolation.md)를 사용합니다. 로컬 검사만으로는 VM이나 서비스가 그 규칙을 적용하는지 확인할 수 없습니다.

## 서로 다른 요구 사항을 가진 두 가지 공개 작업 흐름 {#two-public-flows-different-requirements}

[CodeRabbit Pull Request Reviews](https://docs.coderabbit.ai/overview/pull-request-review)는 pull request(PR)에 이미 제안된 변경에서 시작합니다. [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github)는 개발 작업에서 시작해 새 PR을 제안할 수 있습니다. 두 방식은 서로 다른 작업을 수행합니다. 이 비교는 벤치마크도 아니고 Lamp를 구현하는 두 방식을 비교하는 것도 아닙니다. 여기서는 이 두 작업 흐름만 다루며 CodeRabbit Coding Agent, Copilot code review, 기타 모드는 다루지 않습니다. 제품 테스트 결과가 아니라 2026년 11월 22일에 확인한 공식 문서를 바탕으로 합니다.

| 확인 항목 | CodeRabbit: 기존 PR 검토 | GitHub Copilot cloud agent: 작업 구현 후 PR 제안 |
| --- | --- | --- |
| 입력과 출력 | PR을 열거나 새 커밋을 푸시하면 자동 검토가 시작될 수 있습니다. CodeRabbit은 변경 사항과 저장소의 관련 맥락을 사용하며, 연결된 이슈가 있으면 함께 참고합니다. 발견한 문제와 제안은 기존 PR에 게시합니다. | Agents 탭에서 저장소를 선택하고 Copilot에 작업을 구현해 PR을 열도록 요청합니다. [이슈 할당](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github#assigning-an-issue-to-copilot)으로도 시작할 수 있습니다. Copilot은 이슈 제목, 설명, 기존 댓글, 추가 지침이 있다면 그 지침을 받습니다. Copilot이 새 PR에 들어갈 변경을 만들고 사람이 검토합니다. |
| Tool과 권한 | Linter 같은 [분석 tool](https://docs.coderabbit.ai/tools/index)이 검토 결과에 보탬이 됩니다. 예를 들어 [ESLint 연동](https://docs.coderabbit.ai/tools/eslint)은 승인된 플러그인만 허용합니다. 검토에는 새 브랜치가 필요하지 않지만 [GitHub App 설치](https://docs.coderabbit.ai/platforms/github-com#review-permissions) 시 코드, PR, 검사에 대한 읽기 및 쓰기 권한을 요청합니다. App 권한만으로는 각 분석 tool에 어떤 권한이 주어지는지 알 수 없습니다. | Copilot은 저장소 복사본에서 명령과 테스트를 실행할 수 있습니다. [GitHub 문서](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations#copilot-cloud-agent-can-push-code-changes-to-your-repository)에 따르면, 새 PR을 만들려면 호출자에게 저장소 쓰기 권한이 필요하며 Copilot은 할당된 브랜치로만 푸시할 수 있고 PR을 승인하거나 병합할 수 없습니다. |
| 환경과 격리 | CodeRabbit은 분석을 위해 전체 저장소를 복제하는 [클라우드 sandbox를 설명합니다](https://docs.coderabbit.ai/overview/architecture). 설명에 포함된 그림에는 실행 환경이 여러 종류인 [Cloud Run](https://docs.cloud.google.com/run/docs/about-execution-environments)이 나옵니다. 확인한 자료만으로는 어떤 경계가 적용되는지, 어떤 실행이나 고객이 가동 중인 환경이나 물리 host를 공유할 수 있는지 알 수 없습니다. | **Cloud** 옵션에 대해 GitHub는 사용자 컴퓨터 및 다른 세션과 격리되고 네트워크 제한을 설정할 수 있는 [세션별 Linux sandbox를 설명합니다](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/about-cloud-sandboxes). 이 설명만으로는 경계를 구현하는 기술이나 누가 물리 host를 공유할 수 있는지 알 수 없습니다. |
| 남는 데이터 | CodeRabbit 문서에 따르면 소스와 의존성의 재사용 가능한 [cache](https://docs.coderabbit.ai/reference/caching)가 기본으로 활성화되고 7일 이내에 만료됩니다. [FAQ](https://docs.coderabbit.ai/faq#data-security)에서는 더 오래 보관되는 별도의 검토 맥락을 설명합니다. Cache 만료 시점이 모든 검토 데이터의 삭제 기한을 뜻하지는 않습니다. | [세션 데이터](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/session-data) 문서에서는 중지한 Cloud 세션의 [snapshot](../../glossary/snapshot.md)을 저장해 파일을 복원하고 진행 중이던 작업을 이어갈 수 있다고 설명합니다. 확인한 자료만으로는 모든 사본이 언제 삭제되는지 알 수 없습니다. PR과 커밋은 worker 상태와 별도로 남습니다. |

**적용 범위를 구분해야 합니다.** GitHub는 **Actions** 환경도 문서에서 설명합니다. GitHub가 호스팅하는 Actions 세션은 끝날 때 세션 환경이 폐기되지만 로그는 남습니다. 이 정리 규칙이나 Actions runner의 특성이 기본 **Cloud** 옵션에도 적용된다고 보아서는 안 됩니다.

관리형 서비스를 평가할 때는 선택한 모드, 요금제, 설정에 해당하는 문서를 확인합니다. 무엇이 경계를 넘을 수 있는지, 실행 후 무엇이 남을 수 있는지 기록합니다. 요구하는 특성이 문서에 없다면 제공자에게 근거를 요청하고 더미 데이터로 확인할 수 있는 부분을 검증합니다. “sandbox”라는 말만으로 VM을 쓴다거나, 작업마다 새 환경을 준다거나, 모든 데이터를 삭제한다고 판단하지 않습니다.

다음: [배포 패턴](deployment-patterns.md)에서는 격리 방식의 선택과 배치, 운영 책임, 정리에 관한 결정을 나누어 살펴봅니다.
