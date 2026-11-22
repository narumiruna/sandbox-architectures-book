# Cold boot

Cold boot는 저장해 둔 실행 상태를 재개하는 대신 새 [virtual machine](virtual-machine.md) 안에서 운영 체제를 부팅하여 VM을 시작하는 방식이다. 미리 준비한 disk image를 사용할 수 있으며, cold boot를 하려면 운영 체제를 처음부터 설치해야 하는 것은 아니다.

## 예시

빌드 서비스가 compiler가 이미 들어 있는 disk image에서 Linux sandbox를 시작한다. VM 안에서 Linux가 시작되고, VM 내부의 서비스가 빌드 명령을 받기 시작한다. 이전 VM에서 실행되던 compiler process나 그 밖의 프로그램은 이어받지 않는다.

## 부팅부터 sandbox를 사용할 수 있을 때까지

[virtual machine monitor](virtual-machine-monitor.md)가 가상 하드웨어를 설정한다. [guest kernel](guest.md)이 시작된 다음, guest가 자체 프로그램과 서비스를 시작한다. [revision `42f413d`의 NVX 라이브러리 가이드](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/library.md#cold-boot)는 cold boot의 예를 보여 주고, [저장된 메모리와 VM 상태에서 복원하는 방법](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/library.md#restore-from-a-snapshot)은 별도의 시작 경로로 설명한다.

부팅이 끝나는 시점과 사용할 준비가 되는 시점을 따로 측정한다. Sandbox가 프로젝트 workspace를 연결하거나 첫 명령을 실행할 수 있게 되기 전에 guest의 부팅이 끝날 수도 있다. [cold start](cold-start.md)는 cold boot를 포함할 수 있지만, [snapshot](snapshot.md)을 사용하여 guest 부팅을 건너뛸 수도 있다.

[용어집으로 돌아가기](index.md)
