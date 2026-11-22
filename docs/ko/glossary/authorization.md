# Authorization

authorization은 신원이 확인된 호출자가 특정 리소스에 대해 어떤 작업을 수행해도 되는지 판단하는 것이다. 먼저 호출자가 누구인지 확인해야 하지만, 신원을 안다고 해서 접근 권한이 부여되지는 않는다.

## 예시

script는 issue 조회 [tool](tool.md)을 호출해 `LAMP-17`을 읽을 수 있지만, 다른 프로젝트의 issue는 읽을 수 없다. tool은 요청을 받을 때마다 신원이 확인된 호출자의 권한과 요청 대상 issue를 확인한다. 요청 필드에 다른 프로젝트를 지정한다고 해서 권한이 있다는 증거가 되지는 않는다.

## 확인해야 하는 경우

어떤 작업이 호출자를 대신해 데이터를 반환하거나 변경을 가할 수 있다면 authorization을 확인한다. [sandbox](sandbox.md)는 script가 호출할 수 있는 tool을 제한할 수 있지만, 각 tool은 여전히 해당 호출자가 어떤 작업을 할 수 있는지 확인해야 한다. 구체적인 예시는 [Tool authorization](../practice/design/tool-authorization.md)을 참고한다.

[용어집으로 돌아가기](index.md)
