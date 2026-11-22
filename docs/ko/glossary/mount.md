# Mount

filesystem이나 디렉터리를 mount한다는 것은 그 안의 파일을 특정 경로에서 볼 수 있게 하는 것이다. *bind mount*는 기존 파일이나 디렉터리를 복사하지 않고 다른 경로에서도 볼 수 있게 한다. sandbox가 bind mount를 통해 쓸 수 있다면 원본 파일도 변경할 수 있다.

## 예시

코드 리뷰 sandbox는 `/workspace`에서 host의 프로젝트 디렉터리를 볼 수 있다. 서비스는 이 디렉터리를 sandbox에 읽기 전용으로 mount한다. 리뷰 프로그램은 프로젝트를 검사할 수 있지만 `/workspace`를 통해 변경할 수는 없다. 보고서는 별도의 출력 디렉터리에 쓴다.

## workload에서 볼 수 있는 파일

[mount namespace](namespace.md)를 사용하면 프로세스 그룹마다 무엇이 mount되어 있는지 다르게 보이도록 할 수 있다. Linux [`mount(2)` 문서](https://man7.org/linux/man-pages/man2/mount.2.html)는 mount의 설정과 그 아래의 filesystem을 구분한다. 읽기 전용 bind mount는 해당 mount를 통한 쓰기를 막지만, 다른 mount를 통해 접근할 때도 원본 파일이 읽기 전용이 되는 것은 아니다. 파일의 내용을 숨기지도 않는다. [workload](workload.md)가 볼 필요가 있는 파일만 mount한다.

[용어집으로 돌아가기](index.md)
