# 하드웨어 지원을 받는 Virtual machine {#hardware-backed-virtual-machines}

[virtual machine (VM)](../../glossary/virtual-machine.md)은 [agent](../../glossary/agent.md)에 자체 운영체제 [kernel](../../glossary/kernel.md)을 갖춘 컴퓨터 환경을 제공합니다. VM 안의 프로그램은 운영체제 요청을 [host](../../glossary/host.md) kernel에 직접 보내지 않습니다.

## 누가 요청을 처리하나요? {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md)의 테스트 실행기가 `total.c`를 열기 위해 [system call](../../glossary/system-call.md)을 보내면 [guest kernel](../../glossary/guest.md)이 요청을 처리합니다. Kernel은 guest의 파일 시스템에서 해당 경로를 찾습니다. 프로젝트가 가상 디스크나 공유 디렉터리에 있으면 guest는 그곳에서 프로젝트를 읽을 수 있습니다. 일반 Linux 명령을 실행할 수 있다고 해서 host의 임의 파일을 열 수 있는 것은 아닙니다.

[virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md)는 VM과 guest에 보이는 장치를 관리합니다. 예를 들어 [Firecracker 리비전 `58cf1b2c`](https://github.com/firecracker-microvm/firecracker/blob/58cf1b2cdca407f2323d1b0b25ebb95dfe5b4bcb/docs/design.md)는 Linux guest에 가상 디스크와 네트워크 장치를 제공합니다. [microVM](../../glossary/microvm.md)은 보통 범용 VM보다 적은 수의 장치를 노출합니다. 그래도 guest kernel은 갖고 있습니다. 각 방식의 경계와 장단점을 한눈에 보려면 [VM, container, microVM 비교](../../sandbox-isolation-boundaries.md#compare-a-vm-a-container-and-a-microvm)를 참고하세요.

## 무엇을 계속 공유하나요? {#what-stays-shared}

같은 VM의 [container](../../glossary/container.md) 두 개는 그 VM의 guest kernel을 공유합니다. [pod](../../glossary/pod.md)마다 VM을 하나씩 두는 것과 container마다 VM을 하나씩 두는 것은 다릅니다. 같은 host의 VM은 각각 자체 guest kernel을 실행하더라도 물리 하드웨어를 공유할 수 있습니다. 아키텍처 조사에서 [어떤 workload가 guest kernel을 공유하는지](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel) 비교해 보세요.

## 언제 사용하나요? {#when-to-use-it}

Agent에 완전한 Linux [workspace](../../glossary/workspace.md)가 필요하고 workload에 자체 kernel이 필요할 때 이 경계를 선택합니다. 예를 들어 native 빌드와 테스트 모음을 실행하면서 해당 process가 host kernel에서 직접 실행되지 않게 할 수 있습니다.

## 이 경계가 보호하지 않는 범위 {#what-the-boundary-does-not-cover}

Guest는 host가 노출하기로 한 파일을 사용할 수 있습니다. 쓰기 가능한 공유 프로젝트 디렉터리가 있으면 guest는 그 디렉터리의 host 파일을 변경할 수 있습니다. Guest가 저장소와 네트워크를 통해 각각 무엇에 접근할 수 있는지 확인하세요. [snapshot](../../glossary/snapshot.md)을 재사용한다면 공유하기 전에 디스크 데이터와 메모리 중 무엇이 들어 있는지, 둘 다 들어 있는지 확인하세요.

VMM과 이를 사용하는 sandbox 제품은 [아키텍처 조사](../../agent-sandbox-architectures.md#hardware-backed-linux-environments)를 참고하세요.
