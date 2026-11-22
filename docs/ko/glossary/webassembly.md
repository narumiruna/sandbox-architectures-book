# WebAssembly (Wasm)

WebAssembly는 줄여서 Wasm이라고 하며, 실행 코드의 이식 가능한 형식이다. Wasm [runtime](runtime.md)이 코드에 필요한 기능을 지원하면, 서로 다른 프로세서와 운영 체제에서 같은 코드를 실행할 수 있다. Wasm 자체는 파일 시스템, 네트워크 연결, shell을 제공하지 않는다. 코드가 접근할 수 있는 범위는 [host](host.md)가 무엇을 제공하는지에 달려 있다.

## 예시

로그 서비스가 경고 개수를 세기 위해 명령어와 데이터를 묶은 Wasm module을 실행한다. host가 로그 텍스트를 넘겨주면 module은 개수를 반환한다. module이 로그 파일을 직접 열 필요가 없으므로 서비스는 파일 시스템 접근 권한을 부여하지 않는다.

## 메모리와 import

runtime은 module의 실행 가능한 인스턴스를 만들 때 module의 *imports*를 연결한다. imports는 module이 외부에서 필요로 한다고 선언한 함수나 기타 리소스다. [WebAssembly Core Specification 1.0](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#imports)은 함수뿐 아니라 메모리까지 포함할 수 있는 import를 정의한다. Wasm은 인스턴스가 사용할 수 있는 바이트 범위인 *linear memory*를 읽고 쓴다. [이 범위를 벗어난 접근](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#memory-instructions)은 host 프로세스의 다른 메모리에 닿는 대신 오류와 함께 실행을 중단시킨다.

runtime의 메모리 검사는 [host function](host-function.md)이 미치는 영향을 제한하지 않는다. 파일을 읽는 함수는 호출자가 파일을 직접 읽을 수 없는 경우에도 자체 접근 규칙을 적용해야 한다. host는 맞춤형 함수나 [WebAssembly System Interface (WASI)](webassembly-system-interface.md) 같은 표준 인터페이스를 제공할 수 있다. module을 다른 곳에서 실행하려면 새 환경에서 module에 필요한 Wasm 기능과 import를 지원하는지 확인한다.

## 무엇을 Wasm으로 컴파일하는가?

workload 자체가 Wasm module일 수도 있고, workload를 실행하는 언어 엔진이 module일 수도 있다. [리비전 `9c465268`의 Pi `codemode`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md)는 QuickJS를 Wasm으로 컴파일하고, 자신이 실행하는 JavaScript에 도구를 제공한다. 엔진이 Wasm module이고, 스크립트는 여전히 JavaScript다. 의존성 이름인 [`quickjs-wasi`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/package.json)만으로는 스크립트가 어떤 접근 권한을 받는지 알 수 없다.

## 언제 사용하는가?

운영 체제 전체 대신 일부 host 작업만으로 실행할 수 있는 코드라면 Wasm을 고려한다. 일반 Linux [native binary](native-binary.md)는 Wasm module로 직접 실행할 수 없다. 도구 조회 예시는 [Foundations의 WebAssembly](../isolation/generated-scripts/webassembly.md)를 참조한다.

[용어집으로 돌아가기](index.md)
