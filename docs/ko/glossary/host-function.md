# Host function

host function은 언어 sandbox 밖에서 구현되어 그 안의 코드가 호출할 수 있는 작업이다. sandbox를 실행하는 애플리케이션이 어떤 함수를 노출할지 결정한다. 함수는 호출한 스크립트의 권한만으로 실행되는 것이 아니라, 함수를 구현한 구성 요소의 권한으로 실행된다.

## 예시

[sandbox](sandbox.md) 안의 스크립트에 프로젝트의 버전 번호가 필요하다. 애플리케이션은 해당 프로젝트의 manifest에서 버전을 읽고 버전 문자열만 반환하는 host function을 노출한다. 스크립트는 프로젝트 파일 전반에 대한 접근 권한을 부여받지 않고도 그 값을 얻을 수 있다.

## 경계를 넘는 것

언어 runtime은 이를 둘러싼 애플리케이션의 함수를 호출할 방법을 제공한다. 예를 들어 [WebAssembly](webassembly.md) 모듈은 애플리케이션이 *import*로 제공하는 함수를 호출할 수 있다. import는 모듈 외부에서 제공하는 작업이다. [Wasmtime 보안 문서](https://docs.wasmtime.dev/security.html#webassembly-core)는 명시적으로 제공한 import를 통해 애플리케이션이 모듈 자체의 메모리 밖에서 모듈이 할 수 있는 일을 어떻게 제어하는지 설명한다.

[tool](tool.md)은 agent나 스크립트에 제공하는 작업이다. host function은 언어 sandbox 안에서 그 작업을 호출할 수 있게 하는 방법 중 하나다. 일부 host function은 그 대신 시계와 같은 기본 서비스를 제공한다. 어느 경우든 handler는 입력, 작업의 영향, 반환 데이터에 대해 해당 [policy](policy.md)를 적용해야 한다. 스크립트 자체에 걸린 제한이 handler를 대신해 이 일을 하지는 않는다.

[용어집으로 돌아가기](index.md)
