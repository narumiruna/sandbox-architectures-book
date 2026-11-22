# 운영체제 Process Sandbox {#operating-system-process-sandboxes}

[operating-system process sandbox](../../glossary/operating-system-process-sandbox.md)를 사용하면 [agent](../../glossary/agent.md)는 [host](../../glossary/host.md)의 native 명령을 사용할 수 있지만, 그 명령이 접근할 수 있는 대상은 제한됩니다. Sandbox 안에 별도의 운영체제는 없습니다.

## 누가 요청을 처리하나요? {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md)의 테스트 실행기가 `total.c`를 열어 달라고 요청하면 실행기의 [process](../../glossary/process.md)가 [system call](../../glossary/system-call.md)을 보냅니다. 이 요청은 host [kernel](../../glossary/kernel.md)이 처리합니다. Linux에서는 [mount namespace](../../glossary/namespace.md)를 사용해 process에 프로젝트는 보이되 host의 비공개 디렉터리는 보이지 않게 할 수 있습니다. [seccomp](../../glossary/seccomp.md) 필터는 특정 종류의 system call을 막을 수 있지만, 필터 자체로 개별 파일 경로에 대한 규칙을 적용하지는 못합니다.

예를 들어 [Anthropic Sandbox Runtime 리비전 `0bbebed0`](https://github.com/anthropic-experimental/sandbox-runtime/blob/0bbebed0aa9a8e628dc4df8bc30293550a1988eb/README.md)은 Linux에서 [Bubblewrap](https://github.com/containers/bubblewrap)을, macOS에서 Seatbelt 프로필을 사용합니다. 네트워크 프록시를 사용해 목적지가 허용되는지도 확인합니다. 적용 방식은 host 플랫폼마다 다르므로 agent를 실행할 플랫폼에서 동작을 확인하세요.

## 무엇을 계속 공유하나요? {#what-stays-shared}

Sandbox 안팎의 process는 같은 host kernel을 사용합니다. Kernel은 sandbox마다 보이는 파일 범위를 다르게 설정할 수 있지만, host 디렉터리를 쓰기 가능한 상태로 [mount](../../glossary/mount.md)하면 프로그램은 여전히 그 디렉터리의 파일을 변경할 수 있습니다.

## 언제 사용하나요? {#when-to-use-it}

로컬 agent에 현재 운영체제의 native tool이 필요하지만 host에 대한 무제한 접근 권한까지 물려주면 안 될 때 이 경계를 선택합니다. 개발자가 이미 쓰는 명령줄 tool을 사용하는 테스트 실행기가 이에 해당합니다.

## 이 경계가 보호하지 않는 범위 {#what-the-boundary-does-not-cover}

파일을 숨겨도 process에 이미 전달한 [credential](../../glossary/credential.md)은 없어지지 않으며, 파일 규칙은 네트워크를 제한하지 않습니다. 상속된 환경 변수와 열린 연결을 검토하세요. 무해한 파일과 별도의 네트워크 검사로 [접근 규칙을 확인](../../practice/verification/verifying-access-rules.md)하고, 패키지 관리자가 시작한 테스트 실행기 같은 자식 process에서도 파일 검사를 반복하세요.
