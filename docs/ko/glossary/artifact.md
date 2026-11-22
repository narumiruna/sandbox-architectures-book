# Artifact

artifact는 patch, 테스트 보고서, 빌드 결과처럼 시스템이 작업을 마친 뒤 보관하기로 선택한 출력물이다. [workspace](workspace.md) 전체를 뜻하지는 않는다.

Lamp 작업에서는 수집기가 검토용으로 텍스트 patch와 테스트 출력을 받는다. worker는 즉시 폐기할 수 있으며, 검토용 저장소는 보존 기간이 끝날 때까지 해당 파일을 보관한다. 검토자는 두 파일을 모두 신뢰할 수 없는 출력물로 취급하며, 파일을 읽을 권한이 있어야 한다.

[Workspace와 artifact (영어)](../../practice/data-and-access/workspaces-and-artifacts.md)를 참고한다.
