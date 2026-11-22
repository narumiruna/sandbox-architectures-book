# Kernel-based Virtual Machine (KVM)

Kernel-based Virtual Machine (KVM)은 프로세서의 가상화 기능을 사용해 [virtual machines](virtual-machine.md)를 실행하는 Linux kernel 기능이다. KVM은 [host](host.md)의 소프트웨어에 VM을 만들고 실행할 수 있는 인터페이스를 제공한다. KVM은 [guest kernel](guest.md)도 아니고, VM과 그 장치를 관리하는 프로그램 전체도 아니다.

## 예시

한 빌드 서비스는 Linux host에서 [virtual machine monitor (VMM)](virtual-machine-monitor.md)를 사용해 Linux sandbox를 실행한다. VMM은 KVM으로 guest의 가상 프로세서를 실행하고 빌드에 사용할 가상 디스크를 제공한다. 빌드 도구는 host의 KVM이 아니라 guest kernel에 일반적인 Linux 요청을 보낸다.

## Host 인터페이스

[Linux KVM API](https://docs.kernel.org/virt/kvm/api.html)는 VMM이 `/dev/kvm`을 열고, VM과 가상 프로세서를 만들고, guest 메모리를 설정하는 방법을 설명한다. 선택 기능의 지원 여부는 host에 따라 다르므로 VMM은 어떤 기능을 사용할 수 있는지 조회할 수 있다.

VMM에는 host의 `/dev/kvm`에 접근할 권한이 필요하다. 예를 들어 [리비전 `42f413d`의 NVX Linux/KVM 요구 사항](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#linux--kvm)은 하드웨어 가상화와 해당 장치에 대한 읽기 및 쓰기 권한을 요구한다. 이 권한은 sandbox 안의 workload가 아니라 host에서 실행되는 VMM에 필요하다. 다른 host 인터페이스로는 [MSHV](microsoft-hypervisor.md)와 [WHP](windows-hypervisor-platform.md)를 참고한다.

[용어집으로 돌아가기](../glossary.md)
