# MicroVM vs gVisor

먼저 한 가지를 확인하세요. **작업에 자체 Linux kernel이 필요한가요?** 필요하다면 guest kernel과 장치가 요구 사항을 충족하는 [MicroVM](microvm.md)부터 검토하세요. 필요하지 않다면 호환되는 Linux [container](../../glossary/container.md)를 실행할 후보로 [gVisor](gvisor.md)를 검토하세요. microVM은 [virtual machine](../../glossary/virtual-machine.md)의 한 종류이며, gVisor는 [user-space kernel](../../glossary/user-space-kernel.md)의 한 구현입니다. 이름만으로는 실제 배포 환경에서 어느 쪽이 더 안전하거나 빠른지 알 수 없습니다.

## 실행 경계 비교하기 {#compare-the-execution-boundaries}

프로그램이 파일을 열어 달라고 요청할 때 핵심 차이는 [어느 구성 요소가 요청을 처리하는지](../../sandbox-isolation-boundaries.md#sandboxes-for-operating-system-workloads)입니다. 두 방식 모두 설정에 따라 같은 프로젝트 파일을 제공할 수 있습니다.

| 확인할 사항 | MicroVM | gVisor |
| --- | --- | --- |
| Linux [system call](../../glossary/system-call.md)은 누가 처리하나요? | VM 안에서 실행되는 Linux [guest kernel](../../glossary/guest.md)입니다. | KVM 플랫폼에서도 [Sentry](https://gvisor.dev/docs/architecture_guide/intro/#how-does-gvisor-provide-isolation)가 처리합니다. |
| [host](../../glossary/host.md)는 무엇을 제공해야 하나요? | 하드웨어 지원을 받는 microVM에는 호환되는 가상화 백엔드가 필요합니다. 예를 들어 [Firecracker v1.11.0은 KVM을 사용합니다](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#internal-architecture). | gVisor가 지원하는 Linux host가 필요합니다. [systrap에는 하드웨어 가상화가 필요하지 않지만](https://gvisor.dev/docs/architecture_guide/intro/#how-does-gvisor-provide-isolation), [KVM 플랫폼은 하드웨어 가상화를 사용합니다](https://gvisor.dev/docs/architecture_guide/platforms/#kvm). |
| 작업은 어떤 인터페이스와 자원을 사용할 수 있나요? | 선택한 guest kernel의 인터페이스와 VM이 제공하는 장치를 사용할 수 있습니다. | [gVisor가 구현한 Linux 인터페이스](https://gvisor.dev/docs/user_guide/compatibility/)와 runtime이 제공하는 자원을 사용할 수 있습니다. |
| 어떤 작업이 경계를 공유하나요? | 같은 microVM에 할당된 작업은 guest kernel을 공유합니다. | 같은 gVisor sandbox에 할당된 작업은 Sentry를 공유합니다. |

## 실제 작업 하나로 선택하기 {#make-the-choice-with-one-real-job}

1. **반드시 충족해야 하는 요구 사항을 확인하세요.** Linux kernel의 특정 빌드가 어떻게 동작하는지 검증하는 테스트라면, 그 kernel을 부팅할 수 있는 microVM을 사용하세요. Container 이미지에서 user-space 프로그램을 컴파일하고 테스트하기만 한다면 gVisor도 시험해 보세요. 간단한 동작 확인만으로는 부족합니다. 설치, 빌드, 테스트를 모두 실행하세요.
2. **두 방식에 같은 접근 규칙을 적용해 확인하세요.** 프로젝트의 같은 리비전을 사용하고 각 작업이 허용된 파일, 네트워크 목적지, credential에만 접근하도록 설정하세요. 어떤 작업이 같은 sandbox를 공유하고, 다음 실행으로 무엇이 이어질 수 있는지도 확인하세요. 이는 표에서 비교한 격리 방식과 별도로 결정할 사항입니다.
3. **요구 사항을 충족하는 후보만 측정하세요.** Runtime 버전과 플랫폼을 기록하고, 새로 시작했는지, 저장된 상태에서 복원했는지, 미리 준비된 sandbox를 할당받았는지도 기록하세요. 예상하는 수의 작업을 동시에 실행하면서 첫 명령을 실행할 수 있을 때까지 걸리는 시간, 작업이 끝날 때까지 걸리는 시간, host 메모리 사용량을 [측정](../../practice/verification/measuring-a-sandbox.md)하세요. 한쪽은 새로 시작하고 다른 쪽은 미리 준비된 worker를 쓰면서 그 차이를 격리 방식만의 차이로 해석하지 마세요.

두 방식을 모두 제공하는 실제 시스템은 [Agent Substrate의 아키텍처](../../agent-substrate.md)를 참고하세요.
