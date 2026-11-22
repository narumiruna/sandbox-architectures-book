# gVisor

[gVisor](https://gvisor.dev/docs/architecture_guide/intro/)는 별도의 Linux [guest kernel](../../glossary/guest.md)을 부팅하지 않고 Linux [container](../../glossary/container.md)를 실행합니다. gVisor의 [user-space kernel](../../glossary/user-space-kernel.md)인 **Sentry**가 sandbox 안에서 실행되는 프로그램의 요청을 처리합니다. 다만 gVisor가 Linux 인터페이스를 직접 구현하므로, 일부 기능은 지원하지 않거나 다르게 동작합니다.

## 파일을 열라는 요청은 어디로 가나요? {#where-the-file-request-goes}

1. [Lamp](../../practice/design/from-issue-to-patch.md)의 테스트 실행기는 `total.c`를 열기 위해 [system call](../../glossary/system-call.md)을 보냅니다. Sentry는 sandbox에 보이는 파일 시스템을 기준으로 이 호출을 처리하며, 프로그램의 호출을 [host](../../glossary/host.md) kernel에 그대로 넘기지 않습니다.
2. host 파일을 노출하도록 설정하면 gVisor는 **Gofer**라는 보조 프로세스를 통해 [해당 mount에 대한 접근을 제공할 수 있습니다](https://gvisor.dev/docs/user_guide/filesystem/). 설정에 따라 Gofer가 파일 작업을 하나씩 처리하는 대신 Sentry가 노출된 파일을 직접 다루도록 허용할 수 있습니다. gVisor는 기반 자원을 얻기 위해 여전히 host kernel에 의존합니다. host의 나머지 파일을 숨겨도 sandbox에 의도적으로 mount한 파일은 그대로 보입니다.

## 플랫폼에 따라 무엇이 달라지나요? {#what-changes-with-the-platform}

gVisor의 [플랫폼](https://gvisor.dev/docs/architecture_guide/platforms/)은 Sentry가 호출을 가로채고 프로그램의 실행을 관리할 수 있게 하는 방식입니다. **systrap**은 CPU 가상화 지원이 필요하지 않습니다. **KVM** 플랫폼은 [하드웨어 가상화](hardware-backed-virtual-machines.md)를 사용하지만, Linux 인터페이스를 제공하는 것은 여전히 Sentry입니다. KVM을 사용한다고 해서 gVisor가 자체 Linux kernel을 부팅하는 [MicroVM](microvm.md)이 되는 것은 아닙니다.

## gVisor를 선택하기 전에 확인할 사항 {#what-to-verify-before-choosing-gvisor}

- **Runtime:** gVisor는 [OCI](../../glossary/open-container-initiative.md) [container runtime](../../glossary/container-runtime.md)인 `runsc`를 제공합니다. 배포 환경이 해당 작업에 `runsc`를 사용하는지 확인하세요. Container 이미지만으로는 격리 경계가 정해지지 않습니다.
- **호환성:** [지원하는 Linux 기능](https://gvisor.dev/docs/user_guide/compatibility/)을 확인하세요. 예를 들어 gVisor는 sandbox 내부에서 native 블록 장치를 mount하는 기능을 지원하지 않습니다. 설정과 테스트를 포함한 전체 작업을 실행해 보세요. Shell이 시작된다고 해서 빌드까지 성공하는 것은 아닙니다.
- **공유:** 같은 gVisor sandbox에서 실행되는 프로그램은 Sentry를 공유합니다. 어떤 작업이 같은 sandbox를 공유해도 되는지 정한 뒤, mount, 네트워크 접근, credential에 대한 [접근 규칙을 검증](../../practice/verification/verifying-access-rules.md)하세요.

선택 기준은 [MicroVM vs gVisor](microvm-vs-gvisor.md)를 참고하세요.
