# User-space kernel

User-space kernel은 workload가 운영 체제에 보내는 요청을 [host kernel](kernel.md) 밖에서 처리하는 소프트웨어다. 별도의 guest kernel을 부팅하지 않고도 프로그램이 기대하는 인터페이스를 제공한다. 리소스는 여전히 host kernel에 의존하며, 프로그램이 기대하는 모든 작업을 지원하지는 않을 수 있다.

## 예시

gVisor를 사용하는 빌드 sandbox에서 테스트 프로그램이 자신의 프로세스 ID를 요청한다. [gVisor 아키텍처 가이드](https://gvisor.dev/docs/architecture_guide/intro/)에서 설명하듯이, gVisor의 Sentry는 sandbox 안의 프로그램에 대한 프로세스 ID를 host kernel에 묻는 대신 자체 프로세스 기록을 바탕으로 답한다.

## 호출을 필터링하는 대신 직접 처리

Sentry는 host에 대한 호출을 단순히 허용하거나 거부하는 대신 Linux [system calls](system-call.md)를 구현한다. Sentry는 host kernel에 더 제한된 범위의 요청을 직접 보낼 수 있으며, 이러한 요청이 workload의 호출과 일대일로 대응할 필요는 없다. 이는 프로세스에 허용된 호출을 host kernel이 구현하는 shared-kernel [process sandbox](operating-system-process-sandbox.md)와 다르다. Workload가 Linux에서 직접 실행될 때와 똑같이 동작한다고 가정하지 말고, 필요한 인터페이스와 성능을 테스트해야 한다.

[Glossary로 돌아가기](../glossary.md)
