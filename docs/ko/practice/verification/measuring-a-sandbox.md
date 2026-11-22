# Sandbox의 실행 시간 측정 {#measuring-a-sandbox}

호출자가 첫 출력을 받는 시점**과** 작업이 끝나는 시점을 모두 기록합니다. worker가 빠르게 응답하더라도 컴파일하고 테스트하고 결과를 기록하기까지는 훨씬 오래 걸릴 수 있습니다. 시간을 비교하기 전에 [접근 규칙을 검증합니다](verifying-access-rules.md). 아무리 빨라도 요구 사항을 강제할 수 없는 worker는 후보가 될 수 없습니다.

## 매번 같은 Workload 사용하기 {#use-the-same-workload-each-time}

[Workload](../../glossary/workload.md)는 sandbox가 실행하는 코드와 process를 뜻합니다. 이 실습에서는 접근 검사와 같은 [Lamp 작업](../design/from-issue-to-patch.md)을 사용합니다. `total.c`의 사본에서 뺄셈 오류를 고치고, GCC로 C 프로그램을 빌드하고, 2 더하기 3이 5인지 확인한 뒤 패치와 테스트 로그를 기록합니다. 매번 동일한 [Bubblewrap process sandbox](../../isolation/native-programs/operating-system-process-sandboxes.md)에서 같은 테스트 자료를 사용하며, 서비스 호출이나 인위적인 지연은 없습니다.

| 측정 항목 | 측정을 끝내는 시점 |
| --- | --- |
| 첫 출력까지 걸리는 시간 | 호출자가 `LAMP-17: loaded`를 받을 때입니다. worker는 테스트 자료를 읽은 뒤, 수정한 코드를 컴파일하거나 테스트하기 전에 이 줄을 출력합니다. |
| 완료까지 걸리는 시간 | 호출자가 worker의 출력을 모두 읽고 worker가 종료됐음을 확인할 때입니다. 실행이 성공한 경우에는 프로그램을 빌드하고 테스트를 실행했으며 `change.patch`와 `test.log`를 작성한 상태입니다. |

두 측정 모두 host가 Bubblewrap을 실행하기 직전에 시작하므로 process sandbox를 만들고 Python을 시작하는 시간이 포함됩니다. 실행 전에 입력과 출력 디렉터리를 준비하는 시간, 실행 후 artifact를 확인하고 workspace를 삭제하는 시간, 원격 큐에서 대기하거나 artifact를 전송하는 시간은 **포함하지 않습니다**. 실제 배포 환경에서 이런 단계 때문에 사용자가 더 기다려야 한다면, 그 단계도 측정합니다.

## 새 Sandbox에서 열 번 실행하기 {#run-ten-fresh-launches}

[접근 규칙 검증](verifying-access-rules.md#run-the-local-checks)에 나열된 Linux, Bubblewrap, Python, GCC, `uv` 요구 사항을 따릅니다. 이 책의 체크아웃 루트에서 다음 명령을 실행합니다.

```bash
uv run --offline --no-project --python /usr/bin/python3 python -B examples/lamp/lab.py measure
```

밀리초 단위의 두 시간(`first_output_ms`와 `completion_ms`)이 한 줄에 하나의 쌍으로 표시됩니다. 열 줄에 이어 각 측정 항목의 최솟값, 중앙값, 최댓값이 표시됩니다. 실행기는 매번 종료 상태가 0인지, 예상한 출력 두 줄이 모두 있는지, 패치와 로그가 예상대로 작성됐는지 확인합니다. 실행이 실패하면 그 실행의 시간을 보고하지 않고 실습을 중단합니다.

매번 새 입력 사본, 출력 디렉터리, sandbox를 사용합니다. 실행 사이에 보존되는 빌드 cache는 없으며 host 파일 시스템 cache를 비우거나 추적하지도 않습니다. 이후 실행에서는 컴파일러나 라이브러리를 읽을 때 cache에 남은 데이터를 재사용할 수 있습니다. Sandbox가 새것이라고 해서 host cache가 비어 있다는 뜻은 아닙니다. 다른 후보와 비교한다면 host, kernel, tool 버전, runtime policy, 동시 실행 수준, workspace와 cache를 준비하거나 재사용한 방식을 기록합니다.

## 측정 결과 한 세트 해석하기 {#interpret-one-run}

WSL2의 Ubuntu 26.04.1 LTS 환경(Linux 6.18.33.2, x86-64, AMD Ryzen 9 7950X3D, host 임시 파일은 `tmpfs`에 저장)에서 Bubblewrap 0.11.1, Python 3.14.4, GCC 15.2.0을 사용해 열 번 순서대로 실행했습니다. 실행기는 매번 새 workspace를 만들었습니다. 이 측정 전에 접근 검사를 실행했으며, host cache를 비우거나 추적하지 않았습니다.

| 측정 항목 | 중앙값 | 최솟값–최댓값 |
| --- | ---: | ---: |
| 첫 출력까지 걸리는 시간 | 24.37 ms | 21.49–26.48 ms |
| 완료까지 걸리는 시간 | 62.23 ms | 58.47–63.94 ms |

호출자는 결과가 완성되기 훨씬 전에 첫 줄을 받았습니다. 측정값의 범위를 보면 이처럼 작은 작업도 한 번의 실행만으로는 특성을 파악하기에 부족합니다. 이 결과는 측정 방법의 예시일 뿐, 성능 기준이나 제품 순위가 아닙니다.

실제 후보를 평가할 때는 workload를 고정하고 실행에 어떤 작업이 포함되는지 설명합니다. [Cold start](../../glossary/cold-start.md), [warm pool](../../glossary/warm-pool.md)에서의 할당, [snapshot](../../glossary/snapshot.md) 복원은 같은 작업을 하지 않습니다. 이 예제에서는 VM이나 warm pool, 메모리, 디스크 사용량, 부하가 걸린 상태에서의 시작 시간, artifact 전송을 측정하지 않습니다. Worker의 최대 메모리 사용량을 측정하려면 전용 [control group](../../glossary/control-group.md)이나 이에 상응하는 backend 집계 기능을 사용합니다. Process 하나의 최대 [resident set size](../../glossary/resident-set-size.md)로 측정하지 않습니다. 서비스가 재사용할 수 있는 상태는 [Sandbox의 lifecycle](../operations/sandbox-lifecycle.md)에서, 그 밖의 비교 항목은 [후보 평가 체크리스트](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)에서 확인합니다.

다음: [Sandbox 서비스 확장하기](../operations/scaling-a-sandbox.md)에서는 큐 대기 시간을 비교하고 테스트용 tenant 두 곳을 사용해 새 작업을 시험 환경으로 전환하는 절차를 연습합니다.
