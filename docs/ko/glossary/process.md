# Process

Process는 실행 중인 프로그램의 인스턴스다. [native binary](native-binary.md)는 시스템이 실행할 수 있는 파일이고, process는 시스템이 해당 프로그램을 시작했을 때 실제로 실행되는 것이다. 같은 프로그램을 두 번 실행하더라도 각 실행의 메모리, 열린 파일, 권한은 다를 수 있다.

## 예시

Agent가 Lamp의 테스트 runner를 시작하면 운영 체제는 `total.c`를 열도록 요청할 수 있는 process를 시작한다. Process는 [system call](system-call.md)을 통해 [kernel](kernel.md)에 그 작업을 요청한다. 같은 runner라도 다른 sandbox 구성으로 실행하면 다른 파일들이 보일 수 있다.

## 언제 중요한가

[operating-system process sandbox](operating-system-process-sandbox.md)에서는 host kernel이 실행 중인 process에 제한을 적용한다. 테스트 runner는 child process라고 하는 다른 process를 시작할 수 있다. 제한이 이 process들에도 적용되고, 이들이 필요한 데이터와 열린 파일만 상속하는지 확인한다. 반면 [virtual machine](virtual-machine.md) 안의 process는 VM 자체의 kernel을 사용한다.

파일 요청이 어떤 경로를 거치는지는 [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md#follow-a-request-to-open-a-file)를 참고한다.

[Glossary로 돌아가기](../glossary.md)
