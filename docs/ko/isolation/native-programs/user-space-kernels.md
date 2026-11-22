# User-space kernel 사용 방식 {#user-space-kernels}

[user-space kernel](../../glossary/user-space-kernel.md)을 사용하면 [agent](../../glossary/agent.md)는 별도의 Linux [guest](../../glossary/guest.md)를 부팅하지 않고도 Linux 프로그램을 실행할 수 있습니다. 프로그램이 기대하는 Linux 인터페이스를 구현하므로 프로그램의 요청은 [host](../../glossary/host.md) [kernel](../../glossary/kernel.md)에 바로 전달되지 않습니다.

## 누가 요청을 처리하나요? {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md)의 테스트 실행기가 `total.c`를 열기 위해 [system call](../../glossary/system-call.md)을 보낸다고 가정해 봅시다. [gVisor](https://gvisor.dev/docs/architecture_guide/intro/)에서는 **Sentry**가 이 요청을 처리합니다. Sentry는 실행기에 보이는 파일 시스템에서 해당 경로를 찾습니다. gVisor는 데이터를 가져오기 위해 host에 자체 요청을 보낼 수 있지만, 그 요청의 범위는 제한됩니다. Workload의 system call을 그대로 전달하는 것은 아닙니다.

## 무엇을 계속 공유하나요? {#what-stays-shared}

같은 gVisor sandbox의 프로그램은 Sentry를 공유합니다. gVisor는 기반 자원을 여전히 host kernel에 의존합니다. 반면 [VM](../../glossary/virtual-machine.md)은 guest kernel을 부팅합니다. [process sandbox](operating-system-process-sandboxes.md)에서는 프로그램이 host kernel에 직접 system call을 보냅니다.

## 언제 사용하나요? {#when-to-use-it}

Linux [container](../../glossary/container.md)를 실행해야 하지만 workload와 host kernel 사이에 한 계층을 두고 싶을 때 이 경계를 선택합니다. Linux 인터페이스를 다시 구현하므로 프로그램이 의존하는 기능이 [gVisor에서 지원되지 않거나 다르게 동작할 수 있습니다](https://gvisor.dev/docs/user_guide/compatibility/). 명령이 시작되는지만 보지 말고 실제 설치, 빌드, 테스트 단계를 실행해 확인하세요.

## 이 경계가 보호하지 않는 범위 {#what-the-boundary-does-not-cover}

Sentry는 자신에게 주어진 범위의 파일 시스템을 보여 줍니다. Agent에 어떤 Lamp 데이터를 읽을 권한을 줄지는 Sentry가 결정하지 않습니다. [runtime](../../glossary/runtime.md)이 의도한 [workspace](../../glossary/workspace.md)와 네트워크 접근만 제공하는지 확인하세요.
