# Observability

observability는 시스템이 남긴 기록을 근거로 시스템이 무엇을 했는지 파악할 수 있는 능력이다. sandbox 운영자는 상태 변경 기록, 타임스탬프, 민감한 정보를 가린 로그를 사용해 작업의 어느 부분에서 실패가 발생했는지 알아낼 수 있다.

예를 들어 준비 완료 이벤트가 없고 workspace에서 시간 초과가 발생했다면 provisioning 단계에 문제가 있었음을 시사한다. worker가 준비된 뒤에 컴파일러 진단 메시지가 나왔다면 빌드 단계에 문제가 있었음을 시사한다. 정책에 따른 거부를 명령 실행 오류와 혼동하지 않도록 이러한 기록을 구분해 둔다.

[Observability와 디버깅](../practice/operations/observability-and-debugging.md)을 참고한다.
