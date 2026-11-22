# Warm pool

Warm pool은 요청이 도착하기 전에 준비해 둔 [sandboxes](sandbox.md)의 집합이다. 요청이 들어오면 모든 설정이 끝날 때까지 기다리지 않고 그중 하나를 할당받을 수 있다. 사전에 완료되는 작업의 범위는 플랫폼마다 다르며, 준비된 sandbox에도 요청별 설정이 필요할 수 있다.

## 예시

빌드 서비스가 컴파일러가 설치되어 있고 명령 서비스가 실행 중인 미할당 Linux sandbox 세 개를 유지한다. 요청은 그중 하나를 할당받고, 프로젝트 파일을 연결한 뒤, 빌드를 시작한다. 세 개가 모두 할당되면 다음 요청은 기다리거나 [cold start](cold-start.md)를 거칠 수 있다.

## 저장된 파일이 아닌 준비된 인스턴스

[control plane](control-plane.md)은 인스턴스를 준비하고 요청에 할당하며 pool을 다시 채울 수 있다. 예를 들어 [Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/examples/warmpool-quickstart/README.md)는 인스턴스를 준비하는 `SandboxWarmPool`과 그중 하나를 할당받는 `SandboxClaim`을 설명한다. 이러한 수명 주기 관리 방식이 sandbox에서 workload를 격리하는 방법을 결정하지는 않는다.

[snapshot](snapshot.md)은 저장된 상태다. 서비스는 snapshot을 복원해 warm pool을 다시 채울 수 있지만, snapshot만 보관하면 요청이 도착했을 때 여전히 복원 작업을 해야 한다. Pool은 인스턴스가 대기하는 동안 리소스를 점유하는 대신 작업을 미리 처리한다. 할당되지 않은 인스턴스에는 [tenant](tenant.md) 데이터를 두지 말고, 준비 상태를 측정할 때는 할당과 workspace 설정도 고려한다.

[용어집으로 돌아가기](index.md)
