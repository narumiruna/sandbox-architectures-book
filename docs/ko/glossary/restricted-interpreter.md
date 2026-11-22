# Restricted interpreter

Restricted interpreter는 자신이 구현한 언어 기능과 기본 제공 연산만 사용해 코드를 실행한다. 코드는 [host](host.md)가 제공하는 연산을 통해서만 interpreter 외부에 접근할 수 있다. 언어의 기능이 적다고 해서 권한도 제한되는 것은 아니다. host 연산 하나만으로도 넓은 범위의 접근 권한을 줄 수 있다.

## 예시

빌드 서비스는 스크립트가 리스트와 반복문, 그리고 승인된 빌드의 결과를 읽는 [tool](tool.md)을 사용해 실패한 테스트 수를 세도록 한다. 스크립트는 임의의 파일을 열거나 명령을 실행할 수 없다. tool이 결과를 반환하기 전에 서비스는 호출자에게 요청한 빌드의 결과를 읽을 권한이 있는지 확인한다.

## 지원하는 언어와 라이브러리

Interpreter는 자체 규칙에 따라 스크립트를 평가한다. Restricted interpreter는 일부 구문이나 기본 제공 연산을 빼거나 라이브러리를 지원하지 않을 수 있다. 코드가 JavaScript처럼 보여도 일반적인 JavaScript 환경과 같은 패키지나 연산을 지원하는 것은 아니다. 이 방식에는 [WebAssembly](webassembly.md)나 [engine isolate](engine-isolate.md)가 필요하지 않다.

예를 들어 [OpenCode Code Mode의 revision `5310e422`](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md)는 Psychoscript로 JavaScript와 유사한 언어를 해석한다. 이 revision에서는 패키지를 불러오지 않으며 스크립트가 파일 시스템, 네트워크, 프로세스에 직접 접근하도록 허용하지 않는다. Interpreter 외부에서 할 작업에는 host가 tool을 제공한다.

## 언어 외에 적용할 제한

지원하는 반복문도 너무 오래 실행될 수 있고, 승인된 tool 호출도 예상보다 많은 데이터를 반환할 수 있다. 실행 시간, 메모리, tool 사용을 각각 제한한다. 각 tool에 [least privilege](least-privilege.md)를 적용한다. 예를 들어 테스트 결과를 읽는 tool은 임의의 명령을 실행하는 기능까지 제공해서는 안 된다.

[용어집으로 돌아가기](index.md)
