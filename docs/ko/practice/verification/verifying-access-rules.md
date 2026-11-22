# 접근 규칙 검증 {#verifying-access-rules}

허용된 동작이 성공하고, 거부된 동작이 **규칙 때문에** 실패하는지 테스트합니다. 예를 들어 worker가 어떤 파일을 읽을 수 없다면, 먼저 그 파일을 노출했을 때 같은 worker가 읽을 수 있는지 확인합니다. 그렇지 않으면 오타가 있거나 실행을 시작하지 못한 경우에도 규칙이 접근을 막은 것처럼 보일 수 있습니다.

## 결과 예측하기 {#predict-the-results}

이 실습에서는 가상의 [Lamp 이슈 처리 과정](../design/from-issue-to-patch.md)을 사용합니다. 앞서 살펴본 virtual machine 대신 로컬 [operating-system process sandbox](../../glossary/operating-system-process-sandbox.md)를 사용합니다. [Bubblewrap 0.11.1](https://github.com/containers/bubblewrap/blob/v0.11.1/README.md)이 경계를 설정하고, Linux [kernel](../../glossary/kernel.md)이 [policy](../../glossary/policy.md)를 적용합니다. C 프로그램을 빌드할 때는 guest kernel이 아니라 host kernel을 사용합니다.

[Mount](../../glossary/mount.md)는 worker 안에서 host의 경로를 사용할 수 있게 합니다. [Namespace](../../glossary/namespace.md)는 같은 namespace에 속한 process에 특정 자원에 대한 공통된 보기를 제공합니다. 이 보기는 다른 namespace의 보기와 분리됩니다. 검사를 실행하기 전에 실행기가 규칙을 하나씩 바꾸면 다음 결과 중 무엇이 달라질지 예상해 봅니다.

| 확인할 동작 | Worker의 policy를 적용했을 때 예상되는 결과 | 규칙 하나를 바꿨을 때의 비교 결과 |
| --- | --- | --- |
| 할당된 입력을 읽고 결과 쓰기 | Worker가 자신의 Lamp 표식 파일을 읽고, 전용 임시 공간에서 수정한 코드를 빌드 및 테스트하고, `change.patch`와 `test.log`를 저장합니다. | 허용된 동작이므로 비교할 필요가 없습니다. |
| 입력 사본에 쓰기 | 같은 쓰기를 시도하면 `EROFS`(읽기 전용 파일 시스템)가 반환되고 host에 파일이 생기지 않습니다. | 같은 임시 입력을 쓰기 가능하게 mount하면 쓰기가 성공합니다. |
| `/lab/other/marker`에서 다른 workspace 읽기 | 읽기를 시도하면 `ENOENT`(해당 파일이나 디렉터리 없음)가 반환됩니다. Cedar가 mount되지 않았습니다. | 모의 Cedar workspace를 mount하면 같은 경로를 읽을 수 있습니다. |
| Host의 루프백(`127.0.0.1`)에 있는 테스트 서비스에서 모의 응답 읽기 | 연결을 시도하면 `ECONNREFUSED`(연결 거부)가 반환됩니다. Worker의 네트워크 namespace에서 그 포트의 연결을 수신하는 서비스가 없습니다. | 네트워크를 공유하면 같은 주소와 포트에서 `Lamp test service`가 반환됩니다. |

응답을 한 번만 보내는 TCP 서비스는 운영체제가 고른 포트에서 루프백 주소에만 바인딩합니다. 검사가 끝나면 서비스가 종료됩니다. 외부 서비스나 실제 데이터는 사용하지 않습니다. Linux의 [network namespace](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)는 인터페이스, 경로, 포트 번호를 분리합니다. 이 비교에서는 지정한 host 수신 서비스에 접근할 수 있는지만 확인합니다. 외부 접속 목적지 목록이나 운영 환경의 네트워크를 검사하지는 않습니다.

## 로컬 검사 실행하기 {#run-the-local-checks}

x86-64 Linux에서 root가 아닌 계정을 사용합니다. 다음 요구 사항을 미리 갖춥니다.

- 권한 없는 사용자도 user, mount, PID, IPC, UTS, network namespace를 만들 수 있는 환경의 Bubblewrap이 필요합니다. 이 실습은 `/usr/bin/bwrap` 버전 0.11.1로 테스트했습니다. Host나 바깥쪽 container가 namespace 생성을 막을 수 있습니다.
- `/bin`, `/lib`, `/lib64`가 `/usr` 아래를 가리키는 통합 `/usr` 시스템이 필요합니다. Sandbox는 `/usr/bin/python3`(Python 3.14.4로 테스트)과 `/usr/bin/gcc`를 사용하며, 시스템의 어셈블러, 링커, C 개발 헤더도 사용합니다(GCC 15.2.0으로 테스트).
- Host 스크립트를 실행할 [uv](https://docs.astral.sh/uv/getting-started/installation/)가 필요합니다. 아래 명령은 설치된 Python을 사용하고 프로젝트 설정을 건너뛰며 패키지를 가져오지 않습니다.

이 책의 체크아웃 루트에서 다음 명령을 실행합니다.

```bash
uv run --offline --no-project --python /usr/bin/python3 python -B examples/lamp/lab.py verify
```

`PASS` 줄이 여덟 개 표시되며, 마지막 줄은 다음과 같습니다.

```text
PASS: Lamp compiled and passed its test; change.patch and test.log verified
```

**`EROFS`**, **`ENOENT`**, **`ECONNREFUSED`**가 표시되고 각 비교 검사는 성공하는지 확인합니다. Bubblewrap 설정 중 오류가 나면 실험이 실패한 것이지, 규칙이 접근을 거부했다는 증거가 아닙니다. Host가 namespace 생성을 막거나 필요한 디렉터리 구조가 없다면 호환되는 Linux 테스트 시스템을 사용합니다. 검사를 통과시키려고 격리 옵션을 빼거나 host의 보안 설정을 바꾸거나 예제를 root로 실행하지 않습니다.

[Ubuntu WSL2 테스트 시스템](measuring-a-sandbox.md#interpret-one-run)에서는 검사 여덟 개가 모두 통과했습니다. 실행기는 입력 `total.c`가 바뀌지 않았는지, `change.patch`에서 뺄셈을 덧셈으로 바꿨는지, `test.log`에 `PASS: total(2, 3) = 5`가 포함됐는지 확인했습니다. 이후 임시 파일을 버렸습니다. [테스트 자료와 실행기 소스](https://github.com/narumiruna/sandbox-architectures-book/tree/main/examples/lamp)는 `examples/lamp/`에 있습니다.

## 증거 해석하기 {#interpret-the-evidence}

비교 검사가 성공했다는 것은 파일이 실제로 존재하고, 권한이 있으면 해당 동작이 성공한다는 뜻입니다. 거부를 확인하는 검사는 이 구성에서 worker에 읽기 전용 Lamp 입력을 주고 지정한 Cedar 경로를 숨긴다는 것을 보여 줍니다. 모든 경로, process, 네트워크 경로를 검사한 것은 아닙니다. Worker는 mount된 `/usr`를 읽을 수 있고 여전히 host kernel을 공유합니다. 이 실습은 resource limit을 설정하지 않으며 kernel의 공격 내성, 상속된 비밀 정보, VM 격리, 운영 환경의 tenant identity를 테스트하지 않습니다. 신뢰할 수 있는 테스트 자료만 사용합니다. 실제 배포 환경에서는 실제 runtime, mount, identity 규칙, 허용된 네트워크 목적지를 사용해 검사를 반복합니다. [후보 평가 체크리스트](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)를 참고합니다.

## Tool authorization 별도로 확인하기 {#check-tool-authorization-separately}

Linux의 경계는 누가 [host tool](../../glossary/host-function.md)을 통해 이슈를 읽을 수 있는지 결정하지 않습니다. [Authorization](../../glossary/authorization.md) handler는 별도로 테스트합니다. 아래 예제는 가상 데이터와 [Tool authorization](../design/tool-authorization.md)에서 설명하는 더 단순한 Lamp 프로젝트 전체에 대한 권한 부여를 사용합니다. Bubblewrap 바깥에서 실행되며 이슈 추적기에는 접속하지 않습니다.

```bash
uv run --offline --no-project --python /usr/bin/python3 python - <<'PY'
issues = {("Lamp", "LAMP-17"): "Incorrect item total", ("Cedar", "CEDAR-9"): "Dummy issue"}


def lookup_as_lamp_reviewer(project, issue):
    if project != "Lamp":
        raise PermissionError(project)
    return issues[project, issue]


if lookup_as_lamp_reviewer("Lamp", "LAMP-17") != "Incorrect item total":
    raise SystemExit("FAIL: expected the Lamp issue")
for project, issue, expected in (("Cedar", "CEDAR-9", PermissionError),
                                 ("Lamp", "CEDAR-9", KeyError)):
    try:
        lookup_as_lamp_reviewer(project, issue)
    except expected:
        continue
    raise SystemExit(f"FAIL: {project}/{issue} should fail with {expected.__name__}")
print("PASS: authorized lookup, project denial, and no cross-project fallback")
PY
```

다음: [Sandbox의 실행 시간 측정](measuring-a-sandbox.md)에서는 접근 검사 없이 같은 C workload의 실행 시간을 잽니다.
