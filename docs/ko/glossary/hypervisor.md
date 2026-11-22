# Hypervisor

hypervisor는 [virtual machines](virtual-machine.md)가 물리 컴퓨터의 프로세서와 메모리를 사용하는 방식을 제어하는 소프트웨어다. 일부 프로젝트에서는 *hypervisor*와 *virtual machine monitor*를 같은 뜻으로 쓴다. 이 책에서는 VM과 그 가상 장치를 관리하는 구성 요소를 [virtual machine monitor (VMM)](virtual-machine-monitor.md)라고 부른다.

## 예시

서버가 두 테스트 sandbox를 별도의 VM에서 실행한다. 각 VM에는 자체 가상 프로세서와 메모리가 보인다. hypervisor는 어느 guest에도 상대의 메모리에 직접 접근할 권한을 주지 않으면서 두 VM이 같은 물리 컴퓨터를 사용하게 한다.

## 가상 실행과 접근 policy

하드웨어 지원을 받는 hypervisor는 프로세서 기능을 사용해 guest 명령어를 실행하고 guest가 접근할 수 있는 물리 메모리를 제한한다. VMM은 [KVM](kernel-based-virtual-machine.md) 같은 host 인터페이스를 사용해 이러한 실행을 설정하고 guest 프로그램이 의존하는 장치 동작을 제공할 수 있다. 이러한 역할을 외부에 드러내는 두 가지 방식은 [Linux KVM API](https://docs.kernel.org/virt/kvm/api.html)와 [Microsoft Hypervisor 명세](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/tlfs)를 비교해 보면 알 수 있다.

sandbox에서 프로젝트 디렉터리를 볼 수 있게 할지, 외부 서비스에 연결할 수 있게 할지는 hypervisor가 결정하지 않는다. 이러한 결정은 주변 시스템이 무엇을 노출하고 [policy](policy.md)를 어떻게 적용하는지에 달려 있다.

[용어집으로 돌아가기](../glossary.md)
