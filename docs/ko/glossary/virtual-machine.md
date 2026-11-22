# Virtual machine (VM)

Virtual machine (VM)은 자체 운영 체제에 가상 프로세서, 메모리, 장치를 제공하는 컴퓨터 환경이다. 이 운영 체제에는 자체 [guest kernel](guest.md)이 있다. 하드웨어 지원 VM은 프로세서 기능을 사용해 guest 실행을 [host](host.md)에서 분리하지만, sandbox는 여전히 guest가 일부 host 리소스에 접근하도록 허용할 수 있다.

## 예시

빌드 서비스가 두 작업을 각각 별도의 Linux VM에서 실행한다. 두 작업 모두 각자의 guest 파일 시스템에 패키지를 설치할 수 있다. 서비스가 두 VM에 같은 host 디렉터리의 쓰기 가능한 [mount](mount.md)를 제공하면, 각 작업은 그 디렉터리에서 다른 작업이 사용하는 파일에 여전히 영향을 줄 수 있다.

## VM이 분리하는 것

VM 안에서 프로그램은 파일 열기 같은 서비스를 guest kernel에 요청한다. [hypervisor](hypervisor.md)는 기반 CPU와 메모리의 사용을 제어하고, [virtual machine monitor](virtual-machine-monitor.md)는 VM과 그 가상 장치를 관리한다. 이 방식이 host kernel에서 프로세스를 실행하는 것과 어떻게 다른지는 [Sandbox 격리 경계](../sandbox-isolation-boundaries.md#1-hardware-backed-virtual-machines)를 참조한다.

VM 하나는 workload 하나를 실행하거나 여러 [containers](container.md)를 실행할 수 있다. 이 container들은 파일 시스템을 따로 두면서도 guest kernel을 공유할 수 있다. 무엇에 별도의 VM이 할당되는지, 그리고 이를 둘러싼 sandbox가 어떤 디스크, mount, 네트워크 연결을 노출하는지 확인한다.

[용어집으로 돌아가기](../glossary.md)
