# Guest

guest는 [virtual machine](virtual-machine.md) 안에서 실행되는 운영 체제와 프로그램을 가리킨다. 해당 운영 체제의 핵심인 *guest [kernel](kernel.md)*은 VM이 제공하는 프로세서, 메모리, 장치를 관리한다. guest는 [host](host.md)의 운영 체제 및 kernel과 별개다.

## 예시

sandbox가 Linux guest 안에서 테스트를 실행한다. 테스트가 파일을 열 때는 물리적인 Linux 컴퓨터에서와 마찬가지로 guest kernel에 요청한다. 그 파일이 host 파일을 저장소로 사용하는 가상 디스크에 있더라도, guest에 보이는 것은 디스크이지 host가 그 파일을 보관하는 디렉터리가 아니다.

## guest가 제어하는 범위

guest 프로그램은 guest kernel에 [system calls](system-call.md)를 한다. guest kernel은 VM 안의 프로그램과 파일을 관리한다. [hypervisor](hypervisor.md)와 [virtual machine monitor](virtual-machine-monitor.md)는 가상 하드웨어를 제공하는 과정에서 서로 다른 역할을 맡는다. 예를 들어 [Firecracker v1.11.0의 설계 문서](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md)는 host 파일을 저장소로 사용하는 가상 블록 장치를 설명한다.

guest 내부의 관리자에게 host의 관리자 권한이 자동으로 주어지지는 않는다. 그렇더라도 guest에 의도적으로 노출하는 host 파일, 네트워크 서비스 또는 기타 리소스에는 각각 자체 접근 제어가 필요하다. 같은 VM에 있는 workload는 guest kernel을 공유한다. 이 workload들을 분리해야 한다면 [isolation unit](isolation-unit.md)을 확인한다.

[용어집으로 돌아가기](index.md)
