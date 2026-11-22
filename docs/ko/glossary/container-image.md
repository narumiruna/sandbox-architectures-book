# Container image

Container image는 [container runtime](container-runtime.md)이 [container](container.md)를 시작하는 데 사용하는 파일과 설정의 묶음이다. 프로그램의 실시간 상태가 아니라 시작 환경을 정의한다.

## 예시

빌드 서비스는 Python interpreter와 프로젝트 dependencies가 들어 있는 image 하나를 재사용할 수 있다. 새 container는 모두 같은 파일로 시작할 수 있다. 한 빌드에서 작성한 보고서는 원본 image에 포함되지 않으며, 서비스가 별도로 저장하거나 공유하지 않으면 다른 빌드에 나타나지 않는다.

## 묶음에 들어 있는 내용

[OCI Image Format v1.1.0](https://github.com/opencontainers/image-spec/blob/v1.1.0/manifest.md)은 설정과 filesystem layer를 참조하는 *manifest*로 image를 설명한다. 설정에는 실행할 명령과 같은 기본값을 지정할 수 있다. 각 layer는 filesystem의 변경 사항을 정의하며, image 도구는 이를 순서대로 적용하여 container 시작에 필요한 파일을 준비한다.

Image는 메모리 [snapshot](snapshot.md)처럼 실행 중인 process를 보존하지 않으며, workload를 어떻게 격리할지도 결정하지 않는다. 호환되는 동일한 image를 서로 다른 runtime에서 실행할 수 있다. 코드가 어디까지 접근할 수 있는지 알려면 runtime과 그 policy를 확인한다.

[용어집으로 돌아가기](../glossary.md)
