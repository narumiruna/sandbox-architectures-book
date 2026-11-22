# Resident set size (RSS)

Resident set size는 process의 메모리 중 현재 물리 메모리에 있는 양이다. Peak RSS는 측정 구간에 보고된 값 중 가장 큰 값이다. 이는 process가 예약한 전체 메모리의 양이 아니다.

Launcher의 peak RSS는 작아도 여러 compiler process가 사용하는 메모리를 합하면 더 클 수 있다. 실행 결과를 비교하기 전에 측정 대상이 어느 process 또는 accounting boundary인지 기록한다.

[Sandbox 측정하기 (영어)](../../practice/verification/measuring-a-sandbox.md)를 참고한다.
