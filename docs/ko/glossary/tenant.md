# Tenant

Tenant는 서비스가 작업이나 데이터를 다른 이들의 것과 구분해서 취급하는 사용자, 팀 또는 조직이다. Tenant는 누구의 리소스와 권한이 관련되어 있는지를 나타내며, 실행 중인 코드를 무엇이 분리하는지는 나타내지 않는다. 하나의 tenant에 여러 sandbox 세션이 있을 수 있다.

## 예시

빌드 서비스에 두 팀이 있다. 한 팀은 라이브러리와 문서를 빌드하기 위해 별도의 [sandboxes](sandbox.md)를 각각 시작한다. 다른 팀도 자체 sandbox를 시작한다. 처음 두 sandbox는 같은 tenant에 속하지만, 세 번째 sandbox는 앞의 두 sandbox 중 어느 쪽의 소스 트리나 빌드 결과도 읽을 수 없어야 한다.

## Tenant 간 리소스 분리

[control plane](control-plane.md)은 어느 tenant가 sandbox를 시작하거나 할당받을 수 있는지, 그리고 어느 workspace를 연결하는지 확인한다. 여러 tenant에 서비스를 제공하는 [tool](tool.md)의 handler도 호출자의 tenant가 요청된 데이터를 사용할 수 있는지 확인해야 한다. Handler는 서비스에서 제공하는 신원 정보를 사용해야 하며, 스크립트가 보낸 tenant 이름을 해당 tenant의 리소스 사용 권한으로 간주해서는 안 된다.

Tenant가 반드시 [isolation unit](isolation-unit.md)인 것은 아니다. 서비스는 한 tenant에 작업마다 별도의 VM을 제공할 수 있다. 또한 저장된 출력, 캐시, 복원된 [snapshots](snapshot.md)가 지정된 tenant 범위를 벗어나지 않게 해야 한다. VM을 분리해도 공유 서비스가 다른 tenant의 데이터를 반환하는 문제는 해결되지 않는다.

[Glossary로 돌아가기](index.md)
