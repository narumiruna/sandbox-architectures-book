# Engine isolate

Engine isolate는 JavaScript 같은 언어의 코드를 실행하는 소프트웨어인 언어 엔진 내부의 별도 실행 환경이다. Isolate는 그 안에서 실행되는 스크립트가 만든 객체를 포함해 자체 상태를 갖는다. 여러 isolate가 운영 체제의 프로세스 하나를 공유할 수 있으므로 isolate는 별도의 프로세스나 [virtual machine](virtual-machine.md)이 아니다.

## 예시

이슈 추적기가 두 팀의 스크립트를 서로 다른 isolate에서 실행한다. 한 스크립트가 이슈 제목 목록을 메모리에 보관해도 다른 스크립트는 그 목록을 볼 수 없다. 각 스크립트는 제목을 가져오기 위해 [host function](host-function.md)을 호출한다. 이 함수는 해당 스크립트가 어느 프로젝트를 읽을 권한이 있는지 확인한다.

## 엔진 상태와 host 접근

[V8 13.8.258 Isolate API](https://github.com/v8/v8/blob/13.8.258/include/v8-isolate.h#L277-L285)는 상태를 분리하도록 규정한다. 한 isolate의 V8 객체를 다른 isolate에서 사용해서는 안 된다. 엔진이 이 분리를 관리한다. 엔진을 내장한 애플리케이션인 [host](host.md)는 스크립트에서 호출할 수 있는 작업을 결정한다. [Cloudflare의 Dynamic Workers 아키텍처](https://blog.cloudflare.com/dynamic-workers/)는 이 차이를 보여 준다. 호출자는 스크립트가 선택된 서비스에 이름으로 접근하도록 허용하고, 외부로 직접 보내는 요청은 차단할 수 있다.

Isolate는 host function이 스크립트를 대신해 수행하는 작업을 제한하지 않는다. 스크립트가 접근할 수 있는 각 작업이 그 스크립트의 권한에 맞는지 확인하고, 플랫폼이 CPU와 메모리 사용량을 어떻게 제한하는지도 확인한다. 작업에 네이티브 프로그램 실행이 필요하면 [operating-system process sandbox](operating-system-process-sandbox.md)처럼 이를 지원하는 별도의 환경을 사용한다.

[용어집으로 돌아가기](../glossary.md)
