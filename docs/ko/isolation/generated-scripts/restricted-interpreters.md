# Restricted interpreter 사용 방식 {#restricted-interpreters}

[restricted interpreter](../../glossary/restricted-interpreter.md)는 자체 구현한 언어 기능과 내장 동작만 실행합니다. 스크립트가 호출할 수 있는 추가 동작은 [host](../../glossary/host.md)가 제공합니다. 익숙한 언어 이름이라고 해서 그 언어에서 평소 쓰는 라이브러리나 시스템 API를 쓸 수 있는 것은 아닙니다.

## 누가 요청을 처리하나요? {#who-handles-the-request}

스크립트가 [`LAMP-17`](../../practice/design/from-issue-to-patch.md)의 제목을 요청하면 interpreter는 스크립트를 실행하되 조회는 host의 [tool](../../glossary/tool.md)에 맡깁니다. Tool은 해당 이슈에 대한 [authorization](../../glossary/authorization.md)을 확인한 뒤 제목을 반환합니다. 반복문과 정렬은 interpreter 안에서 실행합니다. 스크립트에는 이슈 추적기 라이브러리나 직접 네트워크에 접근할 권한이 필요하지 않습니다.

[OpenCode 리비전 `5310e422`](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md)는 JavaScript의 일부 기능을 지원하기 위해 Psychoscript를 사용합니다. [Pydantic AI Code Mode](https://pydantic.dev/docs/ai/harness/code-mode/)는 Python의 일부 기능을 지원하기 위해 [Monty(참고 리비전 `5f4a3dfc`)](https://github.com/pydantic/monty/blob/5f4a3dfc493538bb9dc319974393391ba9e7cf14/README.md)를 사용합니다. 둘 다 완전한 언어 환경을 제공하지 않고도 생성된 코드가 tool을 호출할 수 있게 합니다.

## 무엇을 계속 공유하나요? {#what-stays-shared}

Interpreter는 host 애플리케이션의 [process](../../glossary/process.md) 안에서 실행될 수 있습니다. 언어 기능을 제한하는 것만으로 운영체제가 분리되거나 스크립트마다 별도의 process가 생기는 것은 아닙니다. 서로 다른 스크립트가 같은 host tool을 사용할 수도 있습니다.

## 언제 사용하나요? {#when-to-use-it}

스크립트가 주로 tool 호출을 조합하고 결과를 처리할 때 이 경계를 선택합니다. 모델이 생성할 법한 코드로 테스트하세요. 짧고 문법에 맞는 Python이나 JavaScript 코드라도 지원 범위 밖의 기능이나 라이브러리를 사용할 수 있습니다.

## 이 경계가 보호하지 않는 범위 {#what-the-boundary-does-not-cover}

스크립트에 직접 파일 접근 권한이 없어도 제한 없는 쓰기 tool을 호출할 수 있다면 host 파일을 변경할 수 있습니다. Host tool은 별도로 검토하세요. 지원되는 반복문도 너무 오래 실행될 수 있으므로 interpreter가 오래 실행되는 스크립트를 어떻게 중지하는지도 확인하세요.
