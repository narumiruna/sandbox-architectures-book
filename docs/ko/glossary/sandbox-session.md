# Sandbox session

Sandbox session은 [sandbox](sandbox.md) 서비스가 하나의 단위로 추적하는 실행 또는 사용 기간이다. 서비스는 한 session에서 여러 요청을 처리하는 동안 [workspace](workspace.md)와 worker 상태를 유지할 수 있다.

## 예시

Lamp session에는 소스 수정 요청과 테스트 실행 요청이 각각 하나씩 들어 있다. Session이 진행되는 동안 test runner는 수정으로 생긴 변경 사항을 볼 수 있다. 서비스는 session을 종료할 때 workspace를 삭제하더라도 테스트 보고서는 [artifact](artifact.md)로 보관할 수 있다.

## 주의가 필요한 경우

여러 요청에서 session을 재사용할 때는 일시 중지, 재개, 정리를 거쳐도 어떤 파일과 상태가 남는지 확인한다. Session을 종료하면 명령 실행을 멈추고 worker를 해제하면서도 별도 저장소의 결과물은 삭제하지 않을 수 있다.

[Sandbox lifecycle](../practice/operations/sandbox-lifecycle.md)을 참고한다.
