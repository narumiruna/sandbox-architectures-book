# Host

host는 [sandbox](sandbox.md) 외부에서 sandbox에 리소스를 제공하는 시스템이다. [virtual machine](virtual-machine.md)의 경우 일반적으로 VM을 실행하는 컴퓨터나 운영 체제를 뜻한다. 언어 sandbox의 경우 스크립트 엔진을 실행하는 애플리케이션을 뜻할 수 있다. *host*는 특정 경계를 기준으로 한 역할을 가리킨다.

## 예시

빌드 서비스가 서버에서 Linux [guest](guest.md)를 실행한다. host는 CPU 시간과 메모리를 제공하며, 파일을 VM 디스크의 저장소로 사용한다. 팀은 빌드가 host의 복사본을 변경하지 않고 소스 코드를 읽을 수 있도록 읽기 전용 [mount](mount.md)를 통해 프로젝트 디렉터리를 노출하기로 한다.

## 리소스와 접근

host 쪽에서 경계를 설정하고 그 경계를 넘을 방법을 제공한다. VM에는 가상 디스크와 네트워크 연결을 제공할 수 있다. 스크립트 sandbox에는 프로젝트 파일 하나를 읽는 [host function](host-function.md)을 제공할 수 있다. 이런 선택은 workload가 할 수 있는 일에 영향을 준다. 경계가 있다고 해서 리소스에 대한 광범위한 권한을 부여하는 것이 안전해지는 것은 아니다.

host가 반드시 [control plane](control-plane.md)인 것은 아니다. control plane은 sandbox를 어디에 배치할지 결정하고, 다른 컴퓨터가 이를 실행할 수 있다. 설계에서 “host”라고 할 때는 어떤 경계를 기준으로 하는지, 어떤 구성 요소가 실제로 리소스를 제공하는지 확인한다.

[용어집으로 돌아가기](index.md)
