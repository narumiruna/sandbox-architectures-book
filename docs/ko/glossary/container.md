# Container

Container는 하나 이상의 프로그램이 실행될 수 있도록 준비한 환경이다. 프로그램에 사용할 filesystem과 리소스를 제공한다. *Container*라는 말만으로는 무엇이 프로그램과 host를 분리하는지 알 수 없다.

## 예시

코드 리뷰 서비스가 프로젝트에 필요한 compiler와 테스트 도구를 갖춘 container를 시작한다. 두 번째 테스트 작업도 같은 [container image](container-image.md)에서 별도의 container를 시작할 수 있다. Image는 시작에 필요한 파일을 제공한다. 실행 중인 각 container에는 자체 테스트 process가 있으며, 별도의 쓰기 가능한 filesystem이 있을 수도 있다.

## 격리를 제공하는 곳

[container runtime](container-runtime.md)이 환경을 설정한다. Kernel을 공유하는 구성에서 Linux [namespaces](namespace.md)는 각 process에 리소스가 서로 다르게 보이도록 할 수 있고, [control groups](control-group.md)는 리소스 사용량을 집계하거나 제한할 수 있다. Runtime은 [user-space kernel](user-space-kernel.md)로 container를 분리하거나 [virtual machine](virtual-machine.md)에서 실행할 수도 있다. 이러한 방식은 같은 image에서 시작할 수 있지만 [isolation boundaries](isolation-boundary.md)는 서로 다르다.

Runtime이 workload와 무엇을 공유하는지 확인한다. 예를 들어 쓰기 가능한 host [mount](mount.md)가 있으면, container를 어떤 방식으로 패키징했는지와 관계없이 코드가 host 파일을 변경할 수 있다. [VM, container, microVM 비교](../sandbox-isolation-boundaries.md#compare-a-vm-a-container-and-a-microvm)를 참고한다.

[용어집으로 돌아가기](index.md)
