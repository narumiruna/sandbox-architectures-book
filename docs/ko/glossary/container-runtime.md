# Container runtime

Container runtime은 [container](container.md)를 설정하고 실행하는 소프트웨어다. 선택한 격리 설정을 적용하고 프로그램을 시작한다. 두 runtime이 같은 [container image](container-image.md)로 시작하더라도 프로그램에 서로 다른 경계를 적용할 수 있다.

## 예시

빌드 서비스가 테스트 작업에 사용할 sandbox를 시작하도록 runtime에 요청한다. Runtime은 `/workspace`에서 프로젝트를 사용할 수 있게 하고 test runner를 시작한다. 서비스는 작업을 언제 어디서 실행할지 결정하고, runtime은 작업이 실행될 환경을 설정한다.

## 패키지의 파일에서 실행 중인 process까지

Container stack은 image의 파일을 풀고 runtime 설정과 결합하여 *bundle*을 준비할 수 있다. Bundle은 workload를 시작하는 데 필요한 로컬 파일과 설정을 모아 놓은 것이다. [OCI Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/tree/v1.2.1)은 bundle과 create, start 같은 lifecycle 작업을 정의한다. 저수준 runtime은 image를 직접 다운로드하지 않고도 미리 준비된 bundle을 받아 사용할 수 있다.

## Kernel interface를 제공하는 곳

Runtime은 [namespaces](namespace.md)를 사용해 [host kernel](kernel.md)을 직접 이용하거나, [user-space kernel](user-space-kernel.md)을 제공하거나, 자체 kernel이 있는 [virtual machine](virtual-machine.md)에서 workload를 실행할 수 있다. [control plane](control-plane.md)은 workload를 관리하고, runtime의 실행 방식과 설정은 무엇이 workload와 host를 분리하는지 결정한다.

[용어집으로 돌아가기](index.md)
