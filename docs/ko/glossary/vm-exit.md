# VM exit

VM exit는 프로세서가 [guest](guest.md)를 실행하다가 그 guest의 [hypervisor](hypervisor.md)를 실행하는 상태로 전환되는 것을 말한다. VM exit가 발생해도 [virtual machine](virtual-machine.md)은 종료되지 않는다. hypervisor는 이벤트를 처리한 뒤 guest 실행을 재개할 수 있다.

## 예시

guest 드라이버가 가상 장치에 접근한다. 이 접근에서 VM exit가 발생하도록 설정되어 있으면 Linux KVM host에서 CPU는 제어권을 [KVM](kernel-based-virtual-machine.md)에 넘긴다. KVM은 host kernel에서 이벤트를 처리하거나, 장치 동작을 구현하는 [virtual machine monitor (VMM)](virtual-machine-monitor.md)에 제어권을 돌려줄 수 있다.

## guest system call과의 차이

[system call](system-call.md)은 일반적으로 guest를 벗어나지 않고 [privilege level](cpu-privilege-level.md)을 guest 앱에서 guest kernel로 전환한다. VM exit는 guest 경계를 넘는다. 또한 KVM에서는 host의 [`KVM_RUN`](https://docs.kernel.org/virt/kvm/api.html#kvm-run) 호출이 VMM으로 반환되는 것과도 구별된다. 일부 VM exit는 해당 호출이 반환되지 않은 상태에서 처리되고 guest 실행이 재개된다.

[용어집으로 돌아가기](index.md)
