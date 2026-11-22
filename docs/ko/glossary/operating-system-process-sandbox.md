# Operating-system process sandbox

Operating-system process sandbox는 프로그램을 [host kernel](kernel.md)에서 직접 실행하고, 해당 운영 체제의 제어 기능으로 프로그램이 무엇에 접근하고 어떤 작업을 할 수 있는지 제한한다. 별도의 [guest](guest.md) kernel을 시작하지 않는다.

## 예시

로컬 코드 검토 sandbox는 프로젝트에 대한 읽기 권한과 임시 출력 디렉터리에 대한 쓰기 권한을 부여한 상태로 host의 검색 도구를 실행한다. 이 도구에는 별도의 운영 체제가 필요하지 않지만, 도구와 그 child process에는 동일한 제한이 계속 적용되어야 한다.

## 함께 작동하는 제어 기능

Linux에서 [namespaces](namespace.md)는 mount된 filesystem이나 network interface 중 보이는 범위를 제한할 수 있다. [Linux 6.12 Landlock 가이드](https://docs.kernel.org/6.12/userspace-api/landlock.html#layers-of-file-path-access-rights)에 설명된 것과 같은 경로 기반 규칙은 파일 계층에서 수행할 수 있는 작업을 제한할 수 있다. [Seccomp](seccomp.md)는 system call을 필터링할 수 있고, [cgroups](control-group.md)는 리소스 사용량을 측정하고 제한한다. 이 제어 기능들은 서로를 대체할 수 없다. Policy가 무엇을 허용하는지, 그리고 sandbox가 시작하는 프로그램뿐 아니라 그 child process에도 적용되는지 확인한다.

[Glossary로 돌아가기](../glossary.md)
