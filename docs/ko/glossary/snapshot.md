# Snapshot

Snapshot은 시스템이 나중에 복원할 수 있도록 저장한 상태다. 디스크만 담은 snapshot은 저장소의 상태를 보존하지만 실행 중인 프로그램의 상태는 보존하지 않는다. 메모리를 담은 snapshot은 필요한 processor와 device의 상태도 함께 포함하면 실행 중인 상태를 보존할 수 있다. 저장된 메모리에는 [credentials](credential.md)와 기타 비밀 정보가 들어 있을 수 있으므로 민감한 데이터로 취급한다.

## 예시

테스트 서비스는 Linux sandbox를 부팅하고 사용자에게 할당하기 전에 template을 저장한다. 디스크만 담은 snapshot으로는 준비된 파일을 재사용할 수 있지만 Linux를 부팅하고 서비스를 시작해야 한다. 실행 중인 VM의 snapshot으로는 저장 시점부터 해당 서비스를 재개할 수 있다. 어느 경우든 서비스는 새 session을 위해 사용자의 workspace와 접근 권한을 설정해야 한다.

## 복원으로 되살릴 수 있는 상태

Snapshot에 실제로 어떤 파일과 외부 리소스가 보존되는지 확인한다. 예를 들어 [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/snapshotting/snapshot-support.md#overview)은 guest 메모리와 VM 상태를 별도의 파일에 기록한다. VM이 사용하는 실제 디스크는 운영자가 관리하며 기존 네트워크 연결이 유지된다는 보장은 없다. 복원 환경이 호환되는지, snapshot과 일치하는 디스크 상태를 갖추었는지 확인한다.

여러 VM이 하나의 메모리 snapshot에서 재개되면 각각 고유해야 하는 식별자나 기타 값을 그대로 물려받을 수 있다. 2021년 preprint [Restoring Uniqueness in MicroVM Snapshots](https://arxiv.org/abs/2102.12892)은 복원된 instance마다 새로운 상태가 필요한 이유를 설명한다. 공유 template에는 사용자별 데이터와 비밀 정보를 넣지 않는다. 디스크 snapshot에도 파일에 기록된 비밀 정보가 들어 있을 수 있다.

Snapshot은 저장된 artifact이며, 미리 준비된 sandbox의 [warm pool](warm-pool.md)이 아니다. 서비스는 snapshot으로 pool을 채우거나 [cold start](cold-start.md)가 필요할 때 snapshot을 복원할 수 있다.

[용어집으로 돌아가기](index.md)
