# 여러 tenant 간 격리 {#multi-tenant-isolation}

실행 중인 작업을 서로 격리하고, 작업이 끝난 뒤에도 남는 데이터의 접근 권한을 확인하세요. [Lamp 예제](../design/from-issue-to-patch.md)에서 Lamp와 Cedar는 두 [tenant](../../glossary/tenant.md)입니다. Tenant는 작업과 데이터를 다른 그룹과 분리해야 하는 그룹입니다. Cedar는 ID와 파일 이름을 알더라도 Lamp의 이슈, workspace, 검토용 출력을 읽을 수 없어야 합니다.

## 경계를 공유할 대상 정하기 {#decide-what-shares-a-boundary}

[isolation unit](../../glossary/isolation-unit.md)은 [workload](../../glossary/workload.md)의 집합으로, 이 workload는 모두 같은 [isolation boundary](../../glossary/isolation-boundary.md) 인스턴스를 공유합니다. 무엇이 한 인스턴스를 공유할지 정하는 일은 격리 메커니즘을 선택하는 일과 다릅니다. [아키텍처 개요](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)에서는 모두 [virtual machine (VM)](../../glossary/virtual-machine.md)을 사용하더라도 작업을 서로 다르게 묶는 시스템을 비교합니다.

| 경계 하나를 두는 단위 | 장점 | 다음 작업에 이어질 수 있는 상태 |
| --- | --- | --- |
| 요청 | 각 작업을 깨끗한 환경에서 시작할 수 있습니다. | 인스턴스를 교체하면 이전 작업의 상태는 경계 안에 남지 않습니다. 외부 저장소는 여전히 접근 권한을 확인해야 합니다. 작업마다 설정을 반복합니다. |
| Session | 여러 단계에서 편집기, workspace 또는 빌드 출력을 재사용할 수 있습니다. | 같은 session 안에서 요청이 바뀌어도 파일과 process가 유지됩니다. 해당 session에 대한 권한이 있는 호출자만 다시 연결할 수 있습니다. |
| Tenant | 한 tenant의 작업은 오래 유지되는 환경 하나를 사용할 수 있습니다. | 추가 경계가 없으면 해당 tenant의 작업과 사용자가 runtime을 공유합니다. 작업이 그 상태를 공유해도 되는 경우에만 적합합니다. |

## 공유할 자원을 명확히 정하기 {#keep-shared-resources-deliberate}

Lamp는 같은 tenant가 재시도할 때도 빌드를 시도할 때마다 새 VM을 시작합니다. [control plane](../../glossary/control-plane.md)은 요청자의 확인된 identity를 바탕으로 tenant와 실행을 VM에 연결합니다. Workspace 서비스는 이 연결 관계를 확인한 뒤 해당 실행의 일회용 [workspace](../../glossary/workspace.md)를 `/work`에 연결합니다. `lamp/work` 같은 이름은 라벨일 뿐, 권한 확인을 대신하지 않습니다.

작업은 깨끗한 읽기 전용 컴파일러 image를 공유할 수 있습니다. Workspace 디스크, 실행 중인 VM, 쓰기 가능한 캐시(나중에 쓸 입력이나 빌드 결과를 저장하는 곳)는 공유하지 않습니다. 이 예제는 작업 데이터를 연결한 뒤에는 snapshot을 저장하지 않습니다. 나중에 비공개 캐시가 필요해지면 캐시 서비스는 항목을 반환하기 전에 해당 tenant의 접근 권한을 확인해야 합니다.

이슈 처리기는 호출할 때마다 tenant, 동작, 레코드를 확인합니다. 검토 저장소는 읽을 때마다 tenant와 해당 실행에 지정된 검토자를 확인합니다. Lamp의 구성원이라는 사실만으로는 충분하지 않습니다. 실행을 담당하는 운영자가 볼 수 있는 진단 레코드도 tenant 단위로 제한합니다. VM을 분리해도 이러한 저장소가 잘못된 tenant에게 데이터를 넘기는 것까지 막을 수는 없습니다.

## 더미 데이터로 확인하기 {#check-with-dummy-data}

Lamp와 Cedar에 파일 이름은 같지만 서로 다른 식별용 텍스트가 들어 있는 더미 workspace와 artifact를 제공하세요. 각 tenant가 자기 식별용 텍스트는 읽을 수 있지만 다른 tenant의 workspace를 연결하거나 artifact를 가져올 수 없는지 확인하세요. 권한이 있는 Lamp 호출자만 `LAMP-17`을 읽을 수 있는지도 확인하세요. 비공개 캐시가 있다면 같은 이름의 항목에 tenant마다 다른 식별용 값을 넣고, 각각 자기 값만 받는지 확인하세요. Lamp 작업을 실행했던 인프라에서 새 Cedar 작업을 시작하고 Lamp의 식별용 텍스트가 없는지 확인하세요. 로컬 예제는 [접근 규칙 검증](../verification/verifying-access-rules.md)을 참고하세요. 이러한 점검이 host를 공유할 때 생길 수 있는 모든 영향을 다루지는 않습니다.

다음: [Control plane](../operations/control-planes.md)에서는 서비스가 worker를 시작하고 올바른 tenant의 workspace를 연결한 뒤 정리가 끝났는지 확인하는 과정을 살펴봅니다.
