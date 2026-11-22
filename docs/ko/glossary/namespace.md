# Namespace

namespace는 Linux 프로세스 그룹마다 프로세스 ID, mount된 filesystem, 네트워크 인터페이스 같은 시스템 자원을 별도로 볼 수 있게 한다. 프로세스에 별도의 namespace를 제공한다고 해서 별도의 [kernel](kernel.md)이 생기는 것은 아니다.

## 예시

테스트 sandbox는 mount namespace를 사용해 테스트 실행기가 `/workspace`에서 프로젝트 디렉터리를 볼 수 있게 하면서 host의 홈 디렉터리는 보여주지 않는다. 별도의 [process ID namespace](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html)를 사용하면 테스트 실행기가 작업에 속한 프로세스는 볼 수 있지만 host에서 실행 중인 다른 프로세스는 볼 수 없다.

## 보이는 범위를 나누는 것은 권한 규칙이 아니다

Linux는 자원에 따라 [서로 다른 namespace 유형](https://man7.org/linux/man-pages/man7/namespaces.7.html)을 제공한다. 무엇이 mount되어 있는지 바꿔도 workload에 별도의 네트워크가 보이는 것은 아니다. 쓰기 가능한 [mount](mount.md)를 통해 공유된 파일은 권한이 허용하면 여전히 변경할 수 있다.

namespace는 프로세스에 무엇이 보이는지를 정한다. 경로 기반 접근 제어는 프로세스가 파일에 어떤 작업을 할 수 있는지 결정하고, [seccomp](seccomp.md)는 system call을 필터링하며, [control groups](control-group.md)는 자원 사용량을 집계하거나 제한한다.

[용어집으로 돌아가기](../glossary.md)
