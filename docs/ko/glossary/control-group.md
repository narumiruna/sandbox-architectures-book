# Control group (cgroup)

Control group, 줄여서 cgroup은 운영 체제가 CPU 시간이나 메모리처럼 Linux process가 사용하는 리소스를 측정하거나 제한할 수 있도록 process를 하나의 그룹으로 묶는다. Cgroup은 process가 어떤 파일을 열 수 있는지나 어떤 network 목적지에 접근할 수 있는지는 결정하지 않는다.

## 예시

빌드 sandbox가 compiler와 그 worker process를 하나의 cgroup에 넣는다. 서비스는 작업 전체의 메모리 사용량을 측정하고, 작업이 머신의 메모리를 전부 사용하지 못하도록 한도를 설정할 수 있다.

## Linux가 그룹의 리소스를 관리하는 방법

[Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)에서 그룹은 tree 구조를 이룬다. *Controllers*는 각 그룹의 특정 리소스를 관리하는 [kernel](kernel.md) 구성 요소다. 예를 들어 CPU controller는 그룹의 CPU 시간을 제한할 수 있고, memory controller는 그룹의 메모리 사용량을 추적하고 메모리 한도를 적용할 수 있다.

리소스가 서로 다르게 보이도록 하려면 [namespaces](namespace.md)를 사용하고, 파일 및 network 접근을 제어하려면 별도의 [policy](policy.md)를 사용한다. 이러한 제어는 리소스 사용량을 집계하고 제한하는 것과는 역할이 다르다.

[용어집으로 돌아가기](index.md)
