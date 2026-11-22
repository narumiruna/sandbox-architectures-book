# Microsoft Hypervisor (MSHV)

Microsoft Hypervisor는 guest 운영체제가 물리 컴퓨터를 사용하는 방식을 제어하는 소프트웨어다. 이 책에서 *MSHV*는 지원되는 Linux host에서 [virtual machine monitor (VMM)](virtual-machine-monitor.md)가 `/dev/mshv`를 통해 접근할 수 있는 Microsoft Hypervisor backend를 뜻한다. 이 장치는 host 인터페이스이며, [guest kernel](guest.md)이나 VMM 자체가 아니다.

## 예시

한 빌드 서비스는 NVX를 사용해 MSHV가 활성화된 Linux host에서 Linux [microVM](microvm.md) sandbox를 실행한다. Host의 VMM은 `/dev/mshv`를 사용해 VM을 실행한다. VM 안에서 빌드 도구는 여전히 파일을 열고 프로그램을 실행하도록 guest 자체의 Linux kernel에 요청한다.

## Linux 인터페이스를 사용할 수 있는 환경

[Microsoft Hypervisor 명세](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/tlfs)는 격리된 실행 환경을 *partitions*라고 부른다. *Root partition*은 머신을 관리하고 가상화 스택을 실행하는 특권 환경이다. [리비전 `42f413d`의 NVX Linux/MSHV 요구 사항](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#linux--mshv)에 따르면 Linux는 MSHV가 활성화된 kernel을 사용해 그 root partition에서 실행되어야 한다. 이 kernel은 `/dev/mshv`를 제공해야 하며, VMM에는 이 장치를 읽고 쓸 권한이 필요하다. Hypervisor에서 실행되는 일반적인 Linux guest는 이 요구 사항을 충족하지 않는다.

이 Linux backend를 VMM이 Windows에서 사용할 수 있는 host API인 [Windows Hypervisor Platform (WHP)](windows-hypervisor-platform.md)이나, 별개의 Linux host 인터페이스인 [KVM](kernel-based-virtual-machine.md)과 혼동하지 않는다.

[용어집으로 돌아가기](index.md)
