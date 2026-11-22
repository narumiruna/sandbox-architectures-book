# Pod

Pod는 Kubernetes가 배포할 수 있는 가장 작은 단위다. Pod에는 함께 실행되고 네트워크 환경을 공유하며 스토리지를 공유할 수 있는 하나 이상의 [containers](container.md)가 들어 있다. Pod에 반드시 자체 kernel이 있는 것은 아니다. 선택한 runtime이 [isolation boundary](isolation-boundary.md)를 결정한다.

## 예시

테스트 sandbox는 같은 pod에 있는 두 container에서 웹 서버와 테스트 runner를 실행한다. 테스트 runner는 `localhost`에서 서버에 연결할 수 있다. 서비스가 두 container 모두에 공유 출력 디렉터리를 mount하면, 둘 다 그곳에 저장된 테스트 결과를 읽을 수 있다.

## Pod를 공유한다는 의미

[Kubernetes Pods 문서](https://kubernetes.io/docs/concepts/workloads/pods/)에 설명된 표준 모델에서 pod 안의 container들은 IP 주소와 포트 공간을 공유한다. 공유 스토리지는 이를 필요로 하는 container에 설정해야 한다. [virtual machine](virtual-machine.md)을 사용하는 runtime은 pod를 [isolation unit](isolation-unit.md)으로 삼을 수 있다. 예를 들어 [Kata Containers 4.4.0](https://github.com/kata-containers/kata-containers/blob/4.4.0/docs/design/architecture/README.md#kubernetes-support)은 Kubernetes pod를 VM에 넣는다. Pod의 container들은 VM의 guest kernel을 공유하며, 각 container에 별도의 VM이 할당되지는 않는다. 이 방식이 container당 VM 하나를 사용하는 방식과 어떻게 다른지는 [어떤 workload가 guest kernel을 공유하는가](../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)를 참고한다.

[Glossary로 돌아가기](index.md)
