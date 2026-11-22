# CPU privilege level

CPU privilege level은 코드가 프로세서에서 직접 수행할 수 있는 작업을 결정한다. x86-64에서 [operating-system kernel](kernel.md)은 일반적으로 권한이 가장 높은 ring 0에서 실행되며, 애플리케이션은 ring 3의 [user space](user-space.md)에서 실행된다. 애플리케이션은 ring 0 권한을 받지 않고도 [system call](system-call.md)로 kernel에 작업을 요청할 수 있다.

## 예시

Linux 애플리케이션이 파일을 열면 프로세서는 ring 3에서 ring 0으로 전환하고 kernel의 system call 핸들러를 실행하기 시작한다. Kernel은 요청을 확인하고 ring 3에서 실행되는 애플리케이션에 결과를 반환한다.

## Guest 내부의 권한

[Intel VT-x](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)는 [guest](guest.md) 실행(VMX non-root operation)과 [host](host.md) 실행(VMX root operation)을 구분한다. 양쪽 모두 ring 0과 ring 3을 사용할 수 있다. Ring 0에서 실행되는 guest kernel은 같은 guest의 애플리케이션보다 권한이 높지만, 여전히 guest 실행 모드에 있다. Guest의 ring 3에서 guest의 ring 0으로 전환하는 것은 [VM exit](vm-exit.md)가 아니다.

[용어집으로 돌아가기](../glossary.md)
