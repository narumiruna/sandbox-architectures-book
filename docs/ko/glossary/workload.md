# Workload

Workload는 환경이 작업을 수행하기 위해 실행하는 코드와 프로세스다. Sandbox에서는 스크립트 하나, 여러 프로세스를 사용하는 빌드, 또는 agent 세션 전체가 workload일 수 있다. Workload는 실제로 실행되는 것이지, 실행의 출발점이 되는 패키지나 실행을 시작하는 서비스가 아니다.

## 예시

[agent](agent.md)는 어떤 테스트를 실행할지 결정하기 위해 생성된 스크립트를 한 [sandbox](sandbox.md)에서 실행한다. 그런 다음 도구가 별도의 Linux sandbox에서 테스트 실행기와 그 보조 프로세스를 시작한다. 스크립트가 첫 번째 workload이고, 테스트 실행기와 그 보조 프로세스가 두 번째 workload를 이룬다. Agent 자체는 두 sandbox 중 어느 쪽에서도 실행될 필요가 없다.

## 작업에 맞는 경계 선택

Workload에 따라 필요한 실행 환경이 다르다. 여러 도구의 결과를 합치는 스크립트에는 [restricted interpreter](restricted-interpreter.md)만으로 충분할 수 있다. 특정 머신과 운영체제에 맞게 컴파일된 프로그램인 [native binaries](native-binary.md)를 실행하는 빌드에는 해당 프로그램을 실행할 수 있는 호환 환경이 필요하다.

[container image](container-image.md)는 시작에 필요한 파일과 설정을 제공하지만, 실행 중인 workload 자체는 아니다. Workload의 자식 프로세스가 실제로 어디에서 실행되는지, 어떤 리소스에 접근할 수 있는지, 여러 workload가 하나의 [isolation unit](isolation-unit.md)을 공유하는지 확인한다. 작업 유형별로 어떤 환경이 적합한지는 [Sandbox 격리 경계](../sandbox-isolation-boundaries.md)를 참조한다.

[Glossary로 돌아가기](index.md)
