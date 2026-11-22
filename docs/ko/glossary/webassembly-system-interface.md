# WebAssembly System Interface (WASI)

[WebAssembly System Interface (WASI)](https://wasi.dev/)는 파일 읽기나 시간 확인 같은 작업을 위해 host가 [WebAssembly](webassembly.md) 프로그램에 제공할 수 있는 표준 인터페이스 모음이다. WASI는 이런 서비스를 요청하는 방법을 정의한다. WASI는 운영 체제가 아니며, 특정 인터페이스를 지원한다고 해서 그 인터페이스로 표현할 수 있는 모든 리소스에 대한 접근 권한이 부여되지는 않는다.

## 예시

sandbox는 WASI를 통해 보고서 생성기에 테스트 결과가 들어 있는 디렉터리에 대한 읽기 전용 접근 권한을 부여한다. 보고서 생성기는 host의 전체 파일 시스템에 대한 접근 권한을 받지 않고도 그 결과를 읽을 수 있다. 부여받은 권한이 읽기 전용이므로 해당 디렉터리에 쓸 수는 없다.

## 인터페이스와 권한

Wasm 프로그램은 필요로 하는 인터페이스를 import로 선언한다. 이는 프로그램 외부에서 제공해야 하는 함수나 리소스에 대한 요청이다. host는 이런 인터페이스를 통해 어떤 접근 권한을 부여할지 결정한다. 예를 들어 WASI 0.2.0에서 [filesystem preopens 인터페이스](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/filesystem/preopens.wit)는 프로그램 시작 시 접근 권한을 받은 디렉터리의 목록을 제공한다. [파일 시스템 타입](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/filesystem/types.wit)은 경로가 *handle*이 가리키는 디렉터리 안에 머물도록 요구한다. handle은 파일 시스템 요청에 쓰는 참조다. 접근 플래그로 해당 handle을 통한 변경을 막을 수 있다.

인터페이스 이름만 보지 말고 실제로 부여된 권한을 확인한다. 프로그램은 WASI 외부에서 접근을 제공하는 맞춤형 [host functions](host-function.md)도 받을 수 있다. 이러한 함수에는 자체 권한 검사가 필요하다.

## 버전과 운영 체제 호환성

[WASI Preview 1](https://wasi.dev/releases/wasi-p1)은 `wasi_snapshot_preview1`이라는 이름으로 core Wasm module의 import를 사용한다. [WASI 0.2 (Preview 2)](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/README.md)는 WebAssembly Component Model을 사용한다. 이 모델은 함수와 그 데이터 타입에 이름을 붙이는 언어인 WIT로 기술된 인터페이스를 통해 Wasm component를 연결한다. 프로그램이 필요로 하는 버전과 인터페이스가 [runtime](runtime.md)과 host에서 제공되는지 확인한다. WASI는 Linux kernel을 제공하지 않으며, 일반 Linux [native binary](native-binary.md)를 Wasm으로 실행할 수 있게 해 주지도 않는다.

[용어집으로 돌아가기](index.md)
