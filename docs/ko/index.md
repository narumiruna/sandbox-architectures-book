# Sandbox Architectures Book

[sandbox](glossary/sandbox.md)는 프로그램을 실행하면서 접근할 수 있는 대상을 제한합니다. 이 책에서는 sandbox가 이 제한을 어떻게 적용하는지, 실행할 코드에 맞는 경계를 어떻게 선택하는지 설명합니다.

API 몇 개를 호출하는 AI agent와 패키지를 설치하고 소프트웨어를 빌드하고 테스트를 실행하는 agent에는 서로 다른 환경이 필요합니다. 제품 이름부터 고르지 말고 agent가 할 일부터 살펴보세요.

## 여기서 시작하기 {#start-here}

**기초**부터 읽고, 가상의 코딩 작업인 Lamp가 첫 실행에서 여러 고객이 사용하는 서비스로 발전하는 과정을 따라가 보세요. 격리 방식에 이미 익숙하다면 **sandbox 설계**의 단계별 예제부터 시작하세요.

1. **기초.** [Sandbox의 격리 경계](sandbox-isolation-boundaries.md)에서는 무엇이 접근을 제한하는지 설명합니다. 운영체제에서 workload를 실행하거나 언어 또는 모듈 runtime에서 코드를 실행하는 여섯 가지 방식을 살펴봅니다.
2. **Sandbox 설계.** [이슈에서 패치까지](practice/design/from-issue-to-patch.md)에서는 이슈 조회부터 사람의 검토까지 Lamp 작업의 데이터와 권한을 추적합니다. 그다음 [sandbox를 선택하고](practice/design/choosing-a-sandbox.md) [어디서 실행하고 누가 운영할지](practice/design/deployment-patterns.md) 정하세요.
3. **접근 규칙 설정.** [Tool의 접근 권한 확인](practice/design/tool-authorization.md)부터 읽고, 작업의 각 단계가 사용할 수 있는 파일, 네트워크 endpoint, credential을 정하세요. 고객이나 팀마다 작업과 데이터를 분리하세요.
4. **Sandbox 운영.** [Control plane](practice/operations/control-planes.md)부터 읽고 누가 worker를 시작하고 정리하는지 확인하세요. 이어서 worker의 수명을 관리하고, 자원 사용을 제한하고, 장애를 진단하는 방법을 알아봅니다.
5. **Sandbox 검증.** [접근 규칙이 작동하는지 확인하고](practice/verification/verifying-access-rules.md) [작업의 성능을 측정하세요](practice/verification/measuring-a-sandbox.md). 로컬 실습은 검증 방법을 보여 줄 뿐, 운영 환경의 안전성이나 속도를 보장하지 않습니다.
6. **Sandbox 서비스 확장.** 테스트 고객 두 곳을 두고 [Lamp의 전환을 연습하세요](practice/operations/scaling-a-sandbox.md). worker를 늘려야 하는지, 격리 방식을 바꿔야 하는지, 둘 다 필요한지 확인하세요.

## 참고 자료 활용하기 {#use-the-reference}

- [Agent sandbox 아키텍처](agent-sandbox-architectures.md)는 실제 구현을 비교합니다. workload에 필요한 경계를 파악한 뒤 후보를 찾을 때 활용하세요.
- [용어집](glossary.md)에서는 낯선 용어를 정의하고 자세한 설명으로 연결합니다.

## 책을 읽으며 생각해 볼 질문 {#questions-to-carry-through-the-book}

1. **무엇을 격리해야 하나요?** Tool 스크립트 하나인가요, process 하나인가요, 아니면 Linux workspace 전체인가요?
2. **무엇이 경계를 넘을 수 있나요?** Workload가 어떤 파일, 네트워크 endpoint, credential, tool에 접근할 수 있나요?
3. **실행이 끝나면 무엇이 남나요?** Workspace, snapshot, 캐시에 어떤 데이터가 남나요?
