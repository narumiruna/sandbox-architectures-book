# Code Mode

Code Mode는 모델이 tool을 호출하고 그 결과를 합치는 프로그램을 작성하는 패턴이다. 이 용어는 모델이 tool을 사용하는 방식을 가리키며, 프로그램을 시스템의 나머지 부분과 분리하는 수단을 가리키지는 않는다. 프로그램이 sandbox에서 실행되더라도 tool handler와 agent의 나머지 부분은 그 밖에서 실행될 수 있다.

## 예시

[agent](agent.md)에 미해결 issue가 있는 milestone 목록이 필요하다. agent는 모델에 issue 조회를 하나씩 요청하는 대신, 생성된 script 하나를 [sandbox](sandbox.md)에서 실행한다. script는 각 milestone에 대해 issue 조회 tool을 호출하고, 결과 수를 센 뒤, 짧은 요약을 반환한다. agent는 다음 결정을 내릴 때 그 요약을 사용할 수 있다.

## 생성된 프로그램 실행

애플리케이션은 script가 호출할 수 있는 tool과 script를 실행하는 [runtime](runtime.md)을 선택한다. 예를 들어, [이 책에서 다루는 revision의 Pi `codemode`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md)는 [WebAssembly](webassembly.md)로 컴파일된 QuickJS에서 JavaScript를 실행하며, 애플리케이션이 제공한 tool을 사용할 수 있게 한다. [restricted interpreter](restricted-interpreter.md)에서도 Wasm 없이 Code Mode를 실행할 수 있다.

## tool 호출 검사

script의 경계는 script가 접근할 수 있는 tool을 제한할 수 있다. 그래도 각 [tool](tool.md) handler는 요청된 작업이 허용되는지 확인해야 한다. script에 직접적인 네트워크 접근 권한이 없어도 issue 조회 시에는 프로젝트를 확인해야 한다. 다른 구현은 [아키텍처 개관](../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells)을 참고한다.

[용어집으로 돌아가기](index.md)
