# Seccomp

Seccomp는 프로그램이 kernel에 보내는 요청인 [system calls](system-call.md)을 필터링할 수 있는 Linux 기능이다. 특정 유형의 요청을 차단할 수 있지만, seccomp만으로는 pathname을 기준으로 파일 접근 규칙을 적용하지 않는다.

## 예시

문서 변환 sandbox는 seccomp로 network socket을 만드는 요청을 차단할 수 있다. 생성을 차단하는 것만으로는 프로그램이 이미 가진 socket의 사용을 제한할 수 없다. 별도의 파일 시스템 policy가 변환기가 입력 파일을 읽고 결과를 쓸 수 있는 위치를 제한한다.

## 필터가 검사할 수 있는 정보

[Linux seccomp 필터 문서](https://docs.kernel.org/userspace-api/seccomp_filter.html)에 따르면 필터는 system call 번호와 원시 인자 값을 검사할 수 있다. 필터는 호출을 허용하거나, 예를 들어 호출을 실행하지 않고 실패하게 할 수 있다. `openat` 같은 호출에 전달되는 파일 경로는 프로그램 메모리에 저장된 텍스트다. 필터가 보는 것은 텍스트 자체가 아니라 텍스트의 주소다.

어떤 파일이 보이는지는 [mounts](mount.md)로 제어하고, 그 파일에 할 수 있는 작업은 파일 접근 규칙으로 제어한다. [control group](control-group.md)은 리소스 사용량을 측정하거나 제한하는 별개의 역할을 한다.

[용어집으로 돌아가기](index.md)
