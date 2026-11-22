# User space

User space는 운영 체제의 [kernel](kernel.md) 밖에서 애플리케이션과 대부분의 서비스가 실행되는 영역이다. User space의 프로그램은 kernel보다 하드웨어와 시스템 리소스를 직접 제어할 수 있는 범위가 좁다. 애플리케이션이 user space에서 실행되는 것은 일반적이며, 그것만으로 프로그램이 sandbox에 격리되는 것은 아니다.

## 예시

편집기와 테스트 실행기는 모두 같은 Linux 시스템의 user space에서 실행될 수 있다. 편집기는 사용자에게 접근 권한이 있는 개인 파일을 읽을 수 있다. Sandbox는 테스트 실행기가 프로젝트는 읽을 수 있게 하되, 그 개인 파일은 읽지 못하게 한다. 이 제한은 user space에서 실행되기 때문이 아니라 sandbox에서 적용하기 때문에 생긴다.

## 프로그램이 kernel에 서비스를 요청하는 방식

프로그램은 파일을 열거나 다른 kernel 작업을 수행해야 할 때 [system call](system-call.md)을 하며, 흔히 라이브러리를 거친다. [Linux system call 소개](https://man7.org/linux/man-pages/man2/intro.2.html)에서는 kernel이 요청을 처리하고 결과를 반환하는 방식을 설명한다. [user-space kernel](user-space-kernel.md)은 host kernel 밖에서 그 인터페이스를 소프트웨어로 구현한다.

[Glossary로 돌아가기](index.md)
