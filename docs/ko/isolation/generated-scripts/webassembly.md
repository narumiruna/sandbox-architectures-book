# WebAssembly {#webassembly}

[WebAssembly (Wasm)](../../glossary/webassembly.md)를 사용하면 [host](../../glossary/host.md) 애플리케이션은 메모리 접근을 검사하고 모듈 밖으로 호출할 수 있는 동작을 정해 둔 상태에서 모듈을 실행할 수 있습니다. 모듈을 실행한다고 해서 셸, 파일 시스템, 네트워크 연결이 자동으로 주어지는 것은 아닙니다.

## 누가 요청을 처리하나요? {#who-handles-the-request}

프로그램이 [`LAMP-17`](../../practice/design/from-issue-to-patch.md)의 제목을 요청하면 Wasm [runtime](../../glossary/runtime.md)은 모듈이 애플리케이션에서 이슈 조회용으로 제공한 [host function](../../glossary/host-function.md)을 호출할 수 있게 합니다. Host function은 해당 이슈에 대한 [authorization](../../glossary/authorization.md)을 확인한 뒤 제목을 반환합니다. 제목 정렬은 모듈 안에서 수행할 수 있습니다.

생성된 코드를 이 경계 안에서 실행하는 대표적인 설계는 두 가지입니다.

1. **Workload를 Wasm 모듈로 실행합니다.** 애플리케이션은 workload를 Wasm으로 컴파일해 [Wasmtime](https://docs.wasmtime.dev/security.html) 같은 runtime에서 실행할 수 있습니다. 모듈은 애플리케이션이 제공하는 host 동작을 호출할 수 있습니다.
2. **언어 엔진을 Wasm 모듈로 실행합니다.** [Pi 리비전 `9c465268`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md)에서는 QuickJS를 Wasm으로 컴파일합니다. 모델은 여전히 JavaScript를 작성하고, QuickJS가 그 코드를 해석합니다.

## 무엇을 계속 공유하나요? {#what-stays-shared}

모듈은 같은 host [process](../../glossary/process.md)에서 실행될 수 있지만, 기본적으로 서로의 메모리에는 접근할 수 없습니다. Host는 이슈 조회 서비스 같은 자원을 둘 이상의 모듈에 명시적으로 제공할 수 있습니다.

## 언제 사용하나요? {#when-to-use-it}

Workload나 해당 언어 엔진을 Wasm에서 실행할 수 있고 일반 Linux [native binary](../../glossary/native-binary.md)가 필요 없을 때 이 경계를 선택합니다.

## 이 경계가 보호하지 않는 범위 {#what-the-boundary-does-not-cover}

메모리 접근을 검사하더라도 host function이 모듈을 대신해 할 수 있는 일까지 제한되지는 않습니다. [WebAssembly System Interface (WASI)](../../glossary/webassembly-system-interface.md)가 host 파일 시스템에 대한 접근 권한을 준다고 가정하지 말고, 애플리케이션이 어떤 동작을 제공하는지 확인하세요. Runtime이 메모리를 어떻게 제한하는지, 너무 오래 실행되는 프로그램을 어떻게 중지하는지도 확인하세요.

Tool 스크립트를 실행하는 다른 방법은 [아키텍처 조사](../../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells)를 참고하세요.
