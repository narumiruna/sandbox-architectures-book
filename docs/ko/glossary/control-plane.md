# Control plane

Control plane은 실행 환경을 관리하는 시스템의 일부다. [sandbox](sandbox.md)를 어디에서 실행할지, 언제 시작하거나 중지할지 등을 결정한다. 코드의 동작을 제한하는 메커니즘을 선택하고 설정할 수 있지만, control plane 자체가 그 메커니즘은 아니다.

## 예시

빌드 서비스가 Lamp를 테스트해 달라는 요청을 받는다. 서비스의 control plane은 승인된 설정으로 [virtual machine (VM)](virtual-machine.md)을 시작하고 Lamp의 [workspace](workspace.md)를 연결한 뒤, 실행이 끝나면 VM을 제거한다. 테스트가 실행되는 동안 `total.c`를 열라는 요청은 control plane이 아니라 VM의 [guest kernel](guest.md)이 처리한다.

## 관리와 실행의 차이

Control plane은 실행에 사용할 [runtime](runtime.md)을 선택하고, 특정 workspace를 요청하고, 환경이 준비되었는지 추적할 수 있다. 예를 들어 [Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/README.md)는 Kubernetes 위에서 sandbox를 정의하고 할당받을 수 있는 관리 API를 제공한다. [isolation boundary](isolation-boundary.md)는 runtime이 제공하므로 관리 요청의 종류가 같다고 해서 격리 방식도 같은 것은 아니다.

## 언제 중요한가

많은 작업에 sandbox가 필요하다면 control plane으로 환경을 할당하고 작업이 끝난 뒤 정리한다. 서비스는 누가 환경을 만들거나 할당받을 수 있는지, 누구의 파일을 연결할 수 있는지 [authorization](authorization.md)을 통해 결정해야 한다. Control plane이 다른 [tenant](tenant.md)의 workspace를 sandbox에 잘못 할당하더라도 실행 경계는 그 오류를 바로잡을 수 없다. [패키징, 관리, 격리를 구분하기](../sandbox-isolation-boundaries.md#keep-packaging-management-and-isolation-separate)를 참고한다.

[용어집으로 돌아가기](index.md)
