# MicroVM

microVM은 시작하고 실행하는 데 필요한 작업과 자원을 줄이도록 설계된 [virtual machine](virtual-machine.md)이다. 일반적으로 범용 VM보다 적은 수의 가상 장치를 제공한다. 그래도 자체 운영 체제 [kernel](kernel.md)을 실행한다. microVM이라는 이름이 특정 부팅 시간이나 보안 수준을 보장하지는 않는다.

## 예시

테스트 서비스가 각 작업에 가상 디스크와 네트워크 연결은 있지만 그래픽 표시 장치는 없는 Linux microVM을 제공한다. 작업은 평소 사용하던 명령줄 도구를 실행할 수 있다. microVM이 제공하지 않는 장치가 필요한 workload는 다른 구성이나 실행 환경을 사용해야 한다.

## 가상 장치 수를 줄이면 달라지는 점

microVM용 [virtual machine monitor](virtual-machine-monitor.md)는 실행 대상 workload에 필요하지 않은 장치를 생략할 수 있다. 예를 들어 [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/README.md)은 불필요한 장치와 guest에 제공하는 기능을 생략해 실행에 드는 추가 자원과 guest가 접근할 수 있는 코드의 범위를 줄인다. 제공하는 장치가 적으면 다른 하드웨어를 전제로 하는 workload를 실행하기도 어려워진다.

[isolation unit](isolation-unit.md)은 서비스에 따라 다르다. 하나의 microVM에 작업 하나 또는 여러 workload를 넣을 수 있다. 같은 microVM 안의 workload는 guest kernel을 공유한다. sandbox가 어떤 host 파일과 네트워크 서비스를 노출하는지도 확인해야 한다. VM의 규모가 작다고 해서 허용되는 접근 범위가 정해지는 것은 아니다.

[용어집으로 돌아가기](index.md)
