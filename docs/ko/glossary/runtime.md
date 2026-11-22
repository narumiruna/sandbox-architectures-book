# Runtime

Runtime은 코드를 실행하거나 코드가 실행될 환경을 준비하는 소프트웨어다. 이 용어만으로는 어떤 종류의 코드를 실행할 수 있는지, 무엇이 그 코드를 다른 프로그램과 분리하는지 알 수 없다.

## 예시

Agent 서비스는 [WebAssembly](webassembly.md)로 컴파일한 보고서 생성기를 테스트 결과에 접근할 수 있는 sandbox에서 실행한다. 새 테스트를 실행하려면 서비스는 [container runtime](container-runtime.md)을 통해 빌드용 container를 시작한다. Wasm runtime은 보고서 생성기를 실행하고, container runtime은 native 테스트 프로그램이 실행될 환경을 준비한다.

## Runtime이 실행하거나 준비하는 대상

언어 runtime은 언어 엔진이나 [restricted interpreter](restricted-interpreter.md)로 스크립트를 실행할 수 있다. Wasm runtime은 Wasm 명령과 데이터를 묶은 module을 불러와 실행한다. Runtime이 module의 실행 가능한 instance를 만들 때 애플리케이션은 필요한 [host functions](host-function.md)을 골라 제공할 수 있다. 반면 container runtime은 process가 사용할 파일 시스템과 그 밖의 리소스를 준비한다. 예를 들어 [OCI Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/blob/v1.2.1/runtime.md#lifecycle)은 프로그램을 시작하기 전에 구성 정보를 바탕으로 container 환경을 만드는 과정을 설명한다.

## 관리와 격리는 다르다

[Control plane](control-plane.md)이 sandbox를 어디서 언제 시작할지 결정할 수 있고, runtime은 코드를 실행하거나 실행 환경을 준비한다. 두 역할을 제품 하나가 맡을 수도 있다. [isolation boundary](isolation-boundary.md)를 확인하려면 무엇이 분리를 강제하고 workload가 어떤 host 리소스를 사용할 수 있는지 살펴본다. 예를 들어 container runtime은 host kernel을 공유하는 process를 시작할 수도 있고, 별도의 kernel을 갖춘 VM 안에 process를 배치할 수도 있다.

[용어집으로 돌아가기](../glossary.md)
