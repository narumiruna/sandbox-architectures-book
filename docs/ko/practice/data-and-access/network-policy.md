# 네트워크 policy {#network-policy}

[Lamp 예제](../design/from-issue-to-patch.md)의 worker는 자기 환경 밖의 네트워크 endpoint에 연결하지 않고 빌드와 테스트를 할 수 있습니다. 이슈 tool은 [host](../../glossary/host.md)에 있는 로컬 예제 레코드를 읽습니다. [Workspace 서비스와 artifact 수집기](workspaces-and-artifacts.md)는 실행 전과 후에 일회용 가상 디스크로 입력과 출력을 전달합니다. 둘 다 worker의 네트워크 포트를 사용할 필요가 없습니다.

## 외부로 나가는 연결: 필요한 목적지만 허용하기 {#outbound-allow-only-required-destinations}

[Egress](../../glossary/egress.md)는 worker의 경계 밖으로 나가는 네트워크 트래픽입니다. Host는 Lamp [virtual machine (VM)](../../glossary/virtual-machine.md)에 가상 네트워크 어댑터를 제공하지 않습니다. Worker는 시작할 때 컴파일러, 소스, 테스트를 받으므로 이 설계에는 예외가 필요 없습니다. Worker에서 실행되는 코드는 host 네트워크를 통해 이슈 저장소, 의존성 저장소, 다른 worker, control plane에 접근할 수 없습니다.

나중에 의존성이 필요한 빌드가 생기면 worker에 egress를 허용하는 대신 별도의 가져오기 서비스가 승인된 패키지를 받도록 하세요. 아래 CI 사례에서는 이 권한을 나누는 방법을 보여 줍니다. 미러에 인증이 필요하면 [Credential과 identity](credentials-and-identity.md)에서 설명하는 대로 인증을 worker 밖에서 처리하세요.

클라이언트와 서버를 함께 실행해 확인해야 하는 테스트는 해당 VM 내부에서만 접근할 수 있는 loopback endpoint를 사용할 수 있습니다. 기본 `LAMP-17` 실행에서는 이러한 서비스를 사용하지 않습니다.

## 사례: 패키지가 필요한 CI 작업 {#case-a-ci-job-that-needs-packages}

[continuous integration (CI) 작업](../design/deployment-patterns.md#continuous-integration-ci)이 Lamp의 JavaScript 버전을 테스트한다고 가정해 봅시다. 이 작업은 `LAMP-17`과 달리 기본 image에 없는 패키지가 필요합니다. 필요한 것은 패키지 파일이지, 제한 없는 인터넷 접근이 아닙니다. 테스트 worker는 오프라인 상태로 두고, 가져오기 서비스에만 승인된 미러로 향하는 egress를 허용하세요.

1. **입력을 승인합니다.** 패키지 출처와 무결성 값이 기록된 [npm v11.6.2 lockfile](https://github.com/npm/cli/blob/v11.6.2/docs/lib/content/configuring-npm/package-lock-json.md#packages)을 검토하세요. Lamp가 직접 지정한 패키지만이 아니라 전체 의존성 집합을 확정하세요. 검토하지 않은 패치가 lockfile을 변경했다고 해서 새 패키지를 가져와도 된다는 뜻은 아닙니다.
2. **프로젝트 코드를 실행하지 않고 패키지를 가져옵니다.** 가져오기 서비스가 `deps.lamp.test`에서 승인된 아카이브만 요청하도록 하세요. 이 주소는 승인된 패키지의 사본을 제공하는 가상의 의존성 미러입니다. 미러에 필요한 [credential](../../glossary/credential.md)은 그 서비스 안에 두세요. 허용되지 않은 요청 메서드와 패키지 경로, 승인되지 않은 목적지로의 리디렉션은 거부하세요. 각 아카이브를 준비해 두기 전에 승인된 무결성 값과 일치하는지 확인하세요.
3. **경계 안에서 설치하고 테스트합니다.** 미리 준비한 패키지 캐시 사본을 worker에 따로 제공하세요. 이 사례에서는 설치 스크립트가 필요 없는 패키지를 사용합니다. 캐시가 완전하면 [`npm ci`](https://github.com/npm/cli/blob/v11.6.2/docs/lib/content/commands/npm-ci.md#description)에 [`--offline`](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js#L1353-L1361)과 [`--ignore-scripts`](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js#L860-L872)를 지정해 lockfile에 따라 설치할 수 있습니다. Worker의 경계에서는 계속 네트워크를 차단하세요. 이 옵션은 테스트나 그 자식 process가 할 수 있는 일을 제한하지 않습니다.

완전한 캐시와 불완전한 캐시를 각각 사용해 이 설계를 확인하세요. 승인된 아카이브가 모두 있으면 설치와 테스트가 성공해야 합니다. 하나라도 없으면 레지스트리에 연결하지 않고 설치가 실패해야 합니다. 가져오기 서비스가 승인되지 않은 아카이브를 거부하는지, 승인된 아카이브라도 바이트가 바뀌면 거부하는지, worker가 미러에 직접 연결할 수 없는지도 확인하세요. 이는 CI 배포를 수락하기 위한 점검 항목이지, 로컬 Lamp 실습 결과가 아닙니다.

## 외부에서 들어오는 연결: 미리 보기가 필요한 경우에만 허용하기 {#inbound-no-access-unless-someone-needs-a-preview}

[Ingress](../../glossary/ingress.md)는 경계를 넘어 들어오는 네트워크 트래픽입니다. 가상 네트워크 어댑터가 없으면 다른 환경은 worker에 연결할 수 없습니다. `LAMP-17` 실행에는 미리 보기 URL이나 공개 포트가 없습니다. 검토자는 별도의 검토 저장소에만 연결하며, 그곳에서도 접근 권한이 필요합니다.

나중에 Lamp 작업에 브라우저 미리 보기가 필요하면, 호출자의 identity와 해당 Lamp session에 대한 접근 권한을 확인하는 gateway를 통해 별도의 미리 보기 서비스를 노출하세요. Session이 유지되는 동안 지정된 미리 보기 서비스로만 트래픽을 전달하세요. 외부에서 테스트 endpoint와 worker의 다른 모든 포트에 접근하지 못하게 하세요. 승인된 미리 보기 연결에 응답할 수 있다고 해서 worker가 새 외부 연결을 열 수 있는 것은 아닙니다. 미리 보기 링크만으로 접근 권한을 얻을 수는 없습니다.

[접근 점검](../verification/verifying-access-rules.md)으로 예상한 트래픽과 policy에서 거부해야 할 트래픽을 구분하세요. 점검을 통과하면 확인한 경로에 대한 근거가 되지만, 모든 네트워크 경로를 점검했다는 증거는 아닙니다.

다음: [Credential과 identity](credentials-and-identity.md)에서는 worker에 서비스 비밀 정보를 넘기지 않고, 권한이 있는 읽기만 허용하는 방법을 설명합니다.
