# Agent

agent는 AI 모델을 사용해 다음에 할 일을 결정하고, tool을 호출해 그 일을 수행할 수 있는 시스템이다. agent는 모델에 script를 작성하도록 요청할 수 있지만, 그 script는 agent가 실행할 수 있는 여러 작업 중 하나일 뿐이다. 해당 script를 sandbox에 넣는다고 해서 agent의 나머지 부분도 같은 sandbox에 들어가는 것은 아니다.

## 예시

agent가 프로젝트 현황 보고서를 준비한다. agent는 모델에 issue의 제목을 조회하고 label별로 묶는 script를 작성하도록 요청한다. 이 script는 issue 조회 [tool](tool.md)만 호출할 수 있는 [sandbox](sandbox.md)에서 실행된다. 모델을 호출하는 애플리케이션과 issue 조회를 처리하는 서비스는 둘 다 그 script의 sandbox 밖에서 실행된다.

## agent가 실행하는 것

agent는 모델에 작업을 주고, 모델이 요청한 tool을 실행한 뒤, 다음 결정을 내릴 수 있도록 그 결과를 모델에 돌려줄 수 있다. 한 번에 하나씩 tool 호출을 요청할 수도 있고, [Code Mode](code-mode.md)를 사용해 생성된 script가 여러 번 호출하고 결과를 합치게 할 수도 있다.

다른 설계에서는 agent 애플리케이션 자체와 그 애플리케이션이 실행하는 로컬 명령을 함께 sandbox 안에서 실행한다. 두 설계를 구분하려면 각 [isolation boundary](isolation-boundary.md)에서 어느 코드가 [workload](workload.md)인지 확인한다. 경계 밖의 tool handler는 경계 안에서 요청이 들어와도 자체 권한을 사용한다.

[용어집으로 돌아가기](../glossary.md)
