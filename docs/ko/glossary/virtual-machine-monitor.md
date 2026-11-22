# Virtual machine monitor (VMM)

Virtual machine monitor (VMM)는 [virtual machine](virtual-machine.md)을 생성하거나 관리하고 VM에 virtual device를 제공하는 소프트웨어다. 일부 프로젝트에서는 이 소프트웨어를 [hypervisor](hypervisor.md)라고 부른다. 이 책에서는 VM과 장치 관리를 가리킬 때 *VMM*을 사용하며, sandbox 서비스 전체나 VM 안에서 실행되는 운영 체제는 *VMM*이라고 부르지 않는다.

## 예시

테스트 서비스가 VM을 시작하고 VMM에 virtual disk를 연결해 달라고 요청한다. VM 안의 프로그램은 [guest kernel](guest.md)에 파일을 읽어 달라고 요청한다. VMM은 virtual disk의 동작을 구현하지만, 프로그램의 요청을 guest system call로 직접 받지는 않는다.

## Host 인터페이스와 guest 사이

하드웨어가 지원하는 VM에서 VMM은 host의 virtualization 인터페이스를 통해 guest 메모리와 virtual processor를 구성한다. 또한 guest에 보이는 virtual device를 제공하거나 연결한다. 예를 들어 [Firecracker v1.11.0의 설계 문서](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md)는 [KVM](kernel-based-virtual-machine.md)으로 virtual processor를 실행하고 host의 파일을 기반으로 virtual disk를 제공하는 방식을 설명한다.

Sandbox의 [control plane](control-plane.md)은 VMM을 사용해 VM을 시작하고 중지할 수 있지만, 작업을 어디에서 실행할지 결정하는 일과 누구에게 workspace나 네트워크 접근 권한을 줄지 결정하는 일은 별도의 책임이다. Sandbox가 무엇을 노출하는지 알려면 VMM뿐 아니라 sandbox 전체를 확인해야 한다.

[Glossary로 돌아가기](index.md)
