# Isolation unit

Isolation unit은 하나의 isolation boundary 인스턴스를 공유하는 workload, 즉 실행 중인 작업들의 집합이다. 경계는 특정 계층에서 한 unit을 다른 unit과 분리한다. 경계 자체가 같은 unit 안의 workload를 서로 분리하는 것은 아니다.

## 예시

한 서비스는 Kubernetes [pod](pod.md)마다 별도의 [virtual machine](virtual-machine.md)을 sandbox로 제공한다. 한 pod에는 테스트 실행기와 결과를 수집하는 보조 프로그램이 들어 있다. 두 프로그램은 같은 VM과 그 운영체제의 kernel을 공유한다. 두 번째 pod에는 다른 VM이 할당되므로 VM 경계는 두 pod를 분리할 뿐, 첫 번째 pod 안의 두 프로그램을 분리하지 않는다.

## 이 단위가 가리키는 계층

[Isolation boundary](isolation-boundary.md)는 작업을 *어떻게* 분리하는지 알려 준다. Isolation unit은 경계 인스턴스마다 *어떤 작업*을 한 단위로 분리하는지 알려 준다. Pod마다 VM을 하나씩 두면 pod가 단위이고, container마다 VM을 하나씩 두면 [container](container.md)가 단위다. 세 구현을 비교한 다이어그램은 [어떤 workload가 guest kernel을 공유하는가](../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)를 참고한다.

같은 시스템이라도 다른 계층에서는 더 작은 단위가 있을 수 있다. 한 VM 안의 process마다 서로 다른 파일 시스템이 보이게 할 수 있지만, 그렇다고 process마다 별도의 guest kernel이 생기는 것은 아니다. 두 [tenants](tenant.md)가 guest kernel을 공유해서는 안 된다면, 서비스가 VM을 쓰는지만 보지 말고 [control plane](control-plane.md)이 각 tenant의 workload를 어떻게 배치하는지 확인한다.

[용어집으로 돌아가기](index.md)
