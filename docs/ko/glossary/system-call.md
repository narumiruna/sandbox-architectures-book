# System call (syscall)

System call 또는 syscall은 프로그램이 운영 체제의 [kernel](kernel.md)에 보내는 요청이다. 파일을 열거나 프로세스를 시작하거나 네트워크 소켓을 통해 데이터를 보내는 작업이 프로그램이 이런 방식으로 요청하는 작업의 예다.

## 예시

빌드 sandbox에서 컴파일러가 `/workspace/main.c`를 열어 달라고 요청한다. Shared-kernel sandbox에서는 host kernel이 컴파일러에 보이는 마운트된 파일 시스템을 기준으로 이 경로를 해석하고, 컴파일러가 파일을 열 수 있는지 확인한다. 접근이 거부되면 요청은 실패한다.

## 요청 처리 방식

[Linux system call 소개](https://man7.org/linux/man-pages/man2/intro.2.html)에서 설명하듯이, 프로그램은 흔히 실제 system call을 수행하는 라이브러리 함수를 호출한다. Shared-kernel sandbox에서는 host kernel이 호출을 처리하며 [seccomp](seccomp.md)로 호출을 필터링할 수 있다. [virtual machine](virtual-machine.md)에서는 guest kernel이 그 안의 프로그램에서 들어오는 호출을 처리한다. [user-space kernel](user-space-kernel.md)은 각 요청을 host kernel에 직접 전달하지 않고도 같은 인터페이스를 구현할 수 있다.

[Glossary로 돌아가기](../glossary.md)
