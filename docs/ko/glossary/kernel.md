# Kernel

Kernel은 운영체제의 핵심이다. CPU 시간, 메모리, 파일, 장치 등의 리소스를 관리한다. 프로그램은 파일 열기 같은 작업을 [system calls](system-call.md)를 통해 kernel에 요청한다.

## 예시

같은 Linux 머신에 있는 두 테스트 sandbox에서는 서로 다른 프로젝트 디렉터리가 보이더라도, 각자의 파일을 열 때는 같은 Linux kernel에 요청할 수 있다. 대신 각 sandbox를 별도의 [virtual machine](virtual-machine.md)에서 실행하면, 각 테스트 프로그램은 자기 VM에서 사용할 수 있는 저장 장치에 있는 파일을 열도록 그 VM의 kernel에 요청한다.

## 어느 kernel이 요청을 처리하는가?

일반적인 [operating-system process sandbox](operating-system-process-sandbox.md)는 기반 운영체제의 kernel인 *host kernel*을 사용한다. 이 kernel은 해당 process에 [namespaces](namespace.md)와 [seccomp](seccomp.md) 같은 제어 기능을 적용한다. VM은 자신에게 제공된 리소스를 관리하는 *guest kernel*을 실행한다. [User-space kernel](user-space-kernel.md)은 세 번째 방식을 택한다. workload가 사용하는 kernel 인터페이스를 host kernel 밖에서 소프트웨어로 구현한다. 차이점은 [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md)를 참고한다.

[용어집으로 돌아가기](../glossary.md)
