# Native binary

native binary는 특정 프로세서 유형과 운영 체제 인터페이스에 맞는 명령어로 컴파일된 프로그램이다. 실행하려면 호환되는 환경이 필요하다. Linux native binary는 [WebAssembly](webassembly.md) 모듈이 아니므로 WebAssembly 모듈로 직접 실행할 수 없다.

## 예시

코드 리뷰 sandbox는 64-bit Arm Linux용으로 빌드된 기존 linter를 실행한다. 해당 프로세서 아키텍처와 필수 라이브러리를 갖춘 Linux [virtual machine](virtual-machine.md)에서 실행할 수 있다. linter를 Wasm runtime에서 직접 실행하려면 서비스는 Linux 실행 파일 대신 Wasm 빌드를 제공한다.

## 호환성을 결정하는 요소

실행 파일 형식은 운영 체제에 프로그램을 로드하는 방법을 알려준다. 예를 들어 Linux [ELF 실행 파일](https://man7.org/linux/man-pages/man5/elf.5.html)에는 대상 프로세서 아키텍처가 기록되어 있다. 프로그램이 공유 라이브러리를 사용한다면 실행 환경에는 호환되는 [loader와 라이브러리](https://man7.org/linux/man-pages/man8/ld.so.8.html)도 필요하다. 프로그램의 [system calls](system-call.md)는 실행 환경의 kernel 인터페이스에서 지원해야 한다. 프로세서가 맞는 것만으로는 충분하지 않다.

[용어집으로 돌아가기](index.md)
