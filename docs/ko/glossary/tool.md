# Tool

Tool은 agent나 스크립트가 요청할 수 있는 작업으로, 예를 들어 이슈를 조회하거나 빌드를 시작하는 작업이 있다. 호출자가 입력을 제공하면 handler라는 구성 요소가 작업을 수행한다. Tool을 호출할 권한이 있다고 해서 그 tool에 대한 모든 요청을 허용해야 하는 것은 아니다.

## 예시

릴리스 스크립트가 [sandbox](sandbox.md)에서 실행되며, 이슈의 제목을 가져오기 위해 tool을 호출한다. 스크립트는 이슈 번호를 제공한다. Handler는 해당 이슈가 스크립트에 읽기 권한이 있는 프로젝트에 속하는지 확인하고 제목만 반환한다. Handler는 이슈 서비스에 사용하는 [credential](credential.md)을 스크립트에 넘기지 않고도 해당 서비스를 사용할 수 있다.

## Tool 인터페이스와 handler

Tool 인터페이스는 호출자가 무엇을 요청할 수 있는지 명시한다. Language sandbox에서는 [host function](host-function.md)이 스크립트에서 handler로 이어지는 경로를 제공할 수 있다. Handler는 [policy](policy.md)를 적용한다. 호출자가 해당 리소스에 대해 작업을 수행할 수 있는지 확인한 뒤, 작업의 영향과 결과를 그 범위로 제한한다. 이슈 번호가 유효하다는 것은 형식이 맞다는 뜻이지, 호출자가 그 이슈를 읽을 수 있다는 증거는 아니다.

Sandbox는 스크립트가 호출할 수 있는 tool을 제한할 수 있지만, sandbox 밖에서 실행되는 handler에 스크립트와 같은 제약을 적용할 수는 없다. 빌드 tool은 해당 [workload](workload.md)에 적합한 별도의 sandbox에서 작업을 시작할 수 있다. 그러면 스크립트의 경계와 빌드의 경계가 시스템의 서로 다른 부분을 보호한다.

[Glossary로 돌아가기](../glossary.md)
