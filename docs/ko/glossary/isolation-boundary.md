# Isolation boundary

Isolation boundary는 실행 중인 코드를 다른 코드나 리소스와 분리하는 메커니즘이다. 직접 접근을 차단하면서도 선택한 리소스에는 통제된 경로로 접근할 수 있게 한다. 경계는 메커니즘이고, 무엇이 그 경계를 넘을 수 있는지는 [policy](policy.md)가 정한다. 메커니즘의 이름만으로는 코드가 무엇에 접근할 수 있는지 알 수 없다.

## 예시

Lamp의 테스트 작업은 [virtual machine (VM)](virtual-machine.md)을 기반으로 만든 [sandbox](sandbox.md)에서 실행된다. 서비스는 테스트 실행기에 `total.c`의 복사본을 주거나 쓰기 가능한 공유 경로로 프로젝트를 제공할 수 있다. 두 구성 모두 VM 경계가 있지만, 테스트 작업이 원본 파일을 직접 변경할 수 있는 것은 쓰기 가능한 공유 경로를 사용할 때뿐이다.

## 메커니즘이 분리하는 대상

VM은 guest 운영체제를 [host](host.md)와 분리한다. [Operating-system process sandbox](operating-system-process-sandbox.md)는 host의 [kernel](kernel.md)을 계속 사용하는 [processes](process.md)의 동작을 제한한다. 이와 달리 언어 [runtime](runtime.md)은 스크립트가 특정 작업과 [host functions](host-function.md)만 사용할 수 있게 제한할 수 있다. 전체 비교는 [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md)를 참고한다.

## 언제 중요한가

신뢰할 수 없는 코드를 실행할 환경을 고를 때는 보호해야 할 리소스, policy를 집행하는 구성 요소, 그 구성 요소가 제공하는 접근 경로를 확인한다. 그런 다음 [isolation unit](isolation-unit.md)을 확인한다. 같은 VM에서 실행되는 두 작업은 모두 그 VM 경계 안에 있으므로, 그 경계는 두 작업을 서로 분리하지 않는다.

[용어집으로 돌아가기](../glossary.md)
