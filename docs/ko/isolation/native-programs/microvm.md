# MicroVM

[microVM](../../glossary/microvm.md)은 범용 VM보다 실행에 드는 부가 비용을 줄이도록 설계한 [virtual machine (VM)](../../glossary/virtual-machine.md)입니다. 일반적으로 가상 장치를 더 적게 제공하지만, 자체 운영체제 [kernel](../../glossary/kernel.md)을 실행한다는 점은 같습니다. 작업에 별도의 kernel이 필요하고 제공되는 장치로 충분할 때 선택하세요. 이름에 “Micro”가 들어 있다고 해서 작업이 얼마나 빨리 시작되는지, 메모리를 얼마나 사용하는지 알 수 있는 것은 아닙니다.

## 파일을 열라는 요청은 어디로 가나요? {#where-the-file-request-goes}

1. [Lamp](../../practice/design/from-issue-to-patch.md)의 테스트 실행기가 `total.c`를 열어 달라고 요청합니다. 이 [system call](../../glossary/system-call.md)은 [host](../../glossary/host.md) kernel이 아니라 Linux [guest kernel](../../glossary/guest.md)이 처리합니다.
2. Guest kernel은 자체 파일 시스템에서 경로를 찾습니다. 파일이 가상 디스크에 있으면 필요에 따라 해당 장치에서 데이터를 읽습니다.
3. [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#host-integration)은 host의 파일을 가상 디스크의 저장소로 사용할 수 있습니다. 이 장치를 통해 guest에 보이는 것은 가상 디스크이지 host의 파일 시스템이 아닙니다.

[virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md)인 Firecracker는 가상 장치를 제공하고 [KVM으로 guest CPU를 실행합니다](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#internal-architecture). Firecracker의 [장치 모델](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#machine-model)에는 가상 저장소와 네트워크 장치가 있지만 그래픽 표시 장치는 없습니다. 모든 microVM이 같은 장치를 제공한다고 가정하지 말고, 사용할 VMM을 확인하세요.

## 무엇을 공유하고 무엇을 남길지 결정하기 {#decide-what-to-share-and-keep}

- **Kernel:** 같은 microVM에서 실행되는 프로세스는 guest kernel을 공유합니다. 작업끼리 kernel을 공유하면 안 된다면, 한 microVM에 여러 작업을 넣지 말고 작업마다 별도의 microVM을 할당하세요.
- **상태:** 두 방식이 모두 가능하다면 [cold boot](../../glossary/cold-boot.md)와 [snapshot](../../glossary/snapshot.md) 복원을 비교하세요. 예를 들어 [Firecracker v1.11.0의 snapshot](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/snapshotting/snapshot-support.md#overview)에는 guest 메모리와 에뮬레이션된 하드웨어 상태가 저장됩니다. 가상 디스크의 실제 저장소는 운영자가 별도로 관리합니다. 재사용하기 전에 snapshot과 디스크 양쪽에 작업 데이터가 남아 있는지 확인하세요.
- **접근:** kernel이 분리되어 있어도 guest는 쓰기 가능한 공유 디렉터리에 접근할 수 있으며, 외부로 나가는 트래픽도 자동으로 차단되지 않습니다. 파일, 네트워크 목적지, credential에 대한 규칙을 설정하고 [접근 규칙을 검증](../../practice/verification/verifying-access-rules.md)하세요.

작업에 자체 Linux kernel이 필요하지 않다면 [MicroVM vs gVisor](microvm-vs-gvisor.md)에서 두 방식을 비교해 보세요.
