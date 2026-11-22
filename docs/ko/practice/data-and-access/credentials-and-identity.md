# Credential과 신원 {#credentials-and-identity}

작업에 허용된 동작 하나만 필요하다면 [credential](../../glossary/credential.md), 즉 신원을 증명하거나 접근 권한을 부여하는 값을 건네는 대신 그 동작만 할 수 있게 합니다. [Lamp 예제](../design/from-issue-to-patch.md)에서 host 핸들러는 서비스 credential이 필요 없는 로컬 테스트 데이터를 읽습니다. 서비스는 스크립트와 worker 외부에서 요청자의 신원을 확인합니다. 두 프로그램 모두 요청자의 credential이나 저장소, 이슈 저장소, 검토 저장소에 접근하는 credential을 받지 않습니다.

수집기는 자체 서비스 신원으로 검토 저장소에 씁니다. 검토자는 별도의 신원으로 접수된 출력을 읽습니다. 어느 신원으로도 이 작업 흐름을 통해 수정 사항을 게시할 수 없습니다.

## 변형: 원격 이슈 저장소 {#variant-a-remote-issue-store}

나중에 로컬 테스트 데이터를 원격 이슈 저장소로 바꾼다면 host 핸들러가 중개자 역할을 하게 합니다. 중개자는 호출자를 대신해 승인된 요청을 수행하는 신뢰할 수 있는 구성 요소입니다. 핸들러는 스크립트가 주장하는 프로젝트 이름이 아니라 바깥쪽 서비스가 확인한 신원을 사용합니다. 핸들러는 권한 범위가 좁은 자체 credential로 요청을 보내고 허용된 필드만 반환합니다. 핸들러가 모든 이슈 요청을 받아들인다면 credential을 숨겨도 소용이 없습니다.

Credential을 파일이나 환경 변수로 전달하면 프로그램 코드가 그 값을 복사할 수 있습니다. 만료 시간을 짧게 잡으면 credential이 유효한 기간은 줄어들지만, 복사본이 로그나 저장된 상태에 남는 것까지 막지는 못합니다. 이 변형에서는 핸들러에만 credential을 보관하고, 두 runtime 중 어느 쪽의 파일이나 환경에도 넣지 않습니다.

### 자리표시자 따라가기 {#follow-the-placeholder}

1. 가상의 이슈 저장소가 핸들러에 `<ISSUE_READ_GRANT>`로 표시한 가짜 credential을 발급합니다. 핸들러는 스크립트와 worker의 경계 바깥에 있습니다. 이 credential은 Lamp의 `LAMP-17` 읽기만 허용하며 발급 5분 후에 만료됩니다. 이 credential로 Cedar 이슈를 읽거나 이슈를 수정하거나 저장소 변경 사항을 게시할 수 없습니다.
2. 핸들러는 credential을 사용하기 전에 호출자가 조회할 권한이 있는지 확인합니다. 권한이 없는 요청은 저장소에 접속하지 않고 거부합니다. 저장소는 credential의 범위와 만료 여부를 확인합니다. 핸들러는 만료된 credential을 폐기합니다. 나중에 다시 조회하려면 권한을 다시 확인하고 새 credential을 받아야 합니다.
3. 허용 범위 안의 조회가 만료 전에 성공하고, 저장소가 만료된 credential을 거부하는지 확인합니다. 이 가짜 값이 반환된 이슈 데이터, worker 설정과 파일, 패치, 테스트 출력, 로그(핸들러 로그 포함)에 새어 나오는지 검사합니다. 저장된 [snapshot](../../glossary/snapshot.md)도 검사하고, 메모리를 캡처했다면 그 내용도 확인합니다. 파일을 제거한 뒤에도 메모리 snapshot에 복사본이 남을 수 있습니다. 작업 데이터를 연결하기 전에 worker snapshot을 만들고, 핸들러가 credential을 보유한 동안에는 핸들러의 상태를 캡처하지 않습니다.

다음: [Multi-tenant isolation](multi-tenant-isolation.md)에서는 Lamp와 Cedar가 서로의 데이터를 읽을 수 없도록 이 접근 검사를 어디에서 반복해야 하는지 보여 줍니다.
