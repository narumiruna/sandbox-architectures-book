# Windows Hypervisor Platform (WHP)

Windows Hypervisor Platform (WHP)은 [virtual machine monitor (VMM)](virtual-machine-monitor.md)가 host의 하드웨어 가상화 기능을 사용할 수 있게 하는 Windows 프로그래밍 인터페이스다. WHP는 [host](host.md)에서 제공하는 인터페이스이며, VMM이나 기반 [hypervisor](hypervisor.md), VM 내부에서 실행되는 kernel 자체가 아니다.

## 예시

테스트 서비스가 Windows에서 NVX를 사용해 Linux [microVM](microvm.md) sandbox를 실행한다. host 쪽 VMM은 WHP를 사용해 VM을 실행한다. sandbox 내부의 테스트 프로그램은 Windows API가 아니라 Linux [guest kernel](guest.md)에 파일을 열고 프로그램을 시작해 달라고 요청한다.

## Windows 인터페이스가 제공하는 기능

[Microsoft WHP API](https://learn.microsoft.com/en-us/virtualization/api/)를 사용하면 host 프로그램은 guest를 위한 격리 환경인 *partition*을 만들고, 그 메모리를 구성하며, 가상 프로세서를 만들고 실행할 수 있다. [API 정의](https://learn.microsoft.com/en-us/virtualization/api/hypervisor-platform/hypervisor-platform)는 이러한 작업과 호출자가 플랫폼 기능을 확인하는 방법을 설명한다. VM 구성과 장치 동작은 여전히 VMM이 제공한다.

예를 들어 [리비전 `42f413d`의 NVX Windows/WHP 요구 사항](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#windows--whp)에 따르면 host 펌웨어에서 하드웨어 가상화를 활성화하고 Windows에서 Windows Hypervisor Platform 기능을 활성화한 뒤 재부팅해야 한다. 이 API를 Linux host 인터페이스인 [KVM](kernel-based-virtual-machine.md) 및 [MSHV](microsoft-hypervisor.md)와 혼동하지 않는다.

[용어집으로 돌아가기](index.md)
