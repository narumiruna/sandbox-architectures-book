# Tool 호출 권한 확인 {#tool-authorization}

스크립트에서 [tool](../../glossary/tool.md)을 사용할 수 있다고 해서 모든 호출이 [authorization](../../glossary/authorization.md)을 통과하는 것은 아닙니다. [Lamp 예제](from-issue-to-patch.md)에서 스크립트는 읽기 전용 이슈 tool 하나를 호출할 수 있지만, [host](../../glossary/host.md)는 요청을 하나씩 확인합니다. 스크립트는 Lamp의 이슈 `LAMP-17`을 읽을 수 있지만, Lamp의 다른 이슈나 Cedar의 이슈는 읽을 수 없습니다.

## 스크립트는 어떤 tool을 호출할 수 있습니까? {#which-tools-can-the-script-call}

Host는 조회 스크립트를 [restricted interpreter](../../glossary/restricted-interpreter.md)에서 실행합니다. Tool [allowlist](../../glossary/allowlist.md)에는 프로젝트와 이슈 ID를 인수로 받는 작업인 `get_issue`만 들어 있습니다. 스크립트에는 셸이 없으며, 파일 시스템에 직접 접근하거나 네트워크에 자유롭게 연결할 수도 없습니다. 빌드나 게시를 위한 tool도 제공하지 않습니다. 별도의 Linux worker가 Lamp 프로그램을 컴파일하고 테스트하며, 이 worker에는 이슈 tool을 제공하지 않습니다.

이 목록은 스크립트가 요청할 수 있는 작업의 종류를 제한합니다. 허용된 작업이 어느 프로젝트를 읽을 수 있는지까지 정하지는 않습니다. 읽기 전용 작업도 권한이 없는 호출자에게 데이터를 노출할 수 있습니다.

## 한 번의 호출로 무엇을 할 수 있습니까? {#what-can-one-call-do}

`get_issue`를 구현하는 [host function](../../glossary/host-function.md)은 interpreter 밖에서 실행됩니다. Host는 이번 실행에 이미 승인된 범위, 즉 Lamp의 `LAMP-17` 읽기 권한을 함수에 전달합니다. 스크립트의 인수는 대상을 지정할 뿐 접근 권한을 부여하지 않습니다. 핸들러는 레코드를 조회하기 전에 작업, 프로젝트, 이슈가 허용 범위에 있는지 확인합니다. 승인된 프로젝트와 이슈 ID를 모두 사용해 로컬 테스트 데이터를 읽습니다. 이슈 ID의 접두사만으로는 어느 프로젝트에 속하는지 증명할 수 없습니다.

- **허용:** `get_issue(project="Lamp", issue="LAMP-17")`은 이슈 제목과 잘못된 합계에 관한 보고 내용만 반환합니다. [Credential](../../glossary/credential.md)이나 다른 레코드는 반환하지 않습니다.
- **거부:** `get_issue(project="Cedar", issue="CEDAR-9")`은 프로젝트 검사에서 거부됩니다. Cedar의 테스트 데이터를 읽지 않으며 해당 이슈가 있는지도 알려 주지 않습니다.
- **검색 범위를 넓혀 재시도하지 않기:** `get_issue(project="Lamp", issue="CEDAR-9")`은 이번 실행의 이슈 검사에서 거부됩니다. 대신 tool이 프로젝트 전체를 읽을 수 있도록 설정되어 있더라도 Lamp에서만 검색하고 일치하는 결과가 없다고 응답해야 합니다. 모든 프로젝트를 대상으로 다시 검색하면 안 됩니다.

반환된 이슈 본문은 데이터로 취급합니다. 보고 내용에 다른 프로젝트를 읽으라는 문장이 있어도 host가 부여한 권한은 바뀌지 않습니다.

## 핸들러만 따로 검사하기 {#check-the-handler-on-its-own}

두 프로젝트의 더미 레코드와 Lamp의 `LAMP-17`만 허용하는 실행 컨텍스트로 host 핸들러를 직접 테스트합니다. 허용된 호출은 의도한 필드만 반환하고, 어느 프로젝트에서든 다른 이슈에 대한 호출은 조회 전에 거부되는지 확인합니다. 이 테스트는 interpreter와 별개로 이 핸들러를 검사하는 것이며, 다른 인터페이스의 접근 검사를 검증하지는 않습니다. [로컬 접근 검사](../verification/verifying-access-rules.md)는 실제 이슈 추적 시스템 없이 더 단순한 프로젝트 단위 규칙을 보여 줍니다.

다음: [Workspace와 artifact](../data-and-access/workspaces-and-artifacts.md)에서는 소스 복사본이 worker로 들어가고 텍스트 파일 두 개가 나오는 과정을 살펴봅니다.
