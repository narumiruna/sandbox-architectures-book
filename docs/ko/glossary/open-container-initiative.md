# Open Container Initiative (OCI)

[Open Container Initiative](https://opencontainers.org/)는 container를 패키징하고 배포하고 실행하기 위한 공개 사양을 관리한다. OCI 호환성은 서로 다른 도구가 함께 작동할 수 있게 돕는다. 하지만 실행 중인 프로그램과 host를 무엇이 분리하는지는 알려주지 않는다.

## 예시

빌드 서비스는 컴파일러와 테스트 도구를 OCI [container image](container-image.md)로 패키징한다. 두 backend가 모두 해당 image와 그 안의 프로그램을 지원한다면, 같은 image로 host kernel을 공유하거나 [virtual machine](virtual-machine.md)을 사용하는 테스트 sandbox를 시작할 수 있다.

## 각 사양이 다루는 범위

[Image Specification v1.1.0](https://github.com/opencontainers/image-spec/tree/v1.1.0)은 filesystem 변경 사항과 설정을 담은 패키지를 정의한다. [Distribution Specification v1.1.0](https://github.com/opencontainers/distribution-spec/tree/v1.1.0)은 도구가 container image를 저장하는 서비스인 registry로 콘텐츠를 보내고 registry에서 가져오는 방법을 정의한다. [Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/tree/v1.2.1)은 준비된 container를 실행하는 데 필요한 구성과 수명 주기를 정의한다. 코드가 어디까지 접근할 수 있는지 알아보려면 선택한 [container runtime](container-runtime.md)과 그 설정을 확인한다.

[용어집으로 돌아가기](index.md)
