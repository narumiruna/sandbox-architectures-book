# Extended Page Tables (EPT)

Extended Page Tables (EPT)를 사용하면 [Intel 프로세서](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)가 [guest](guest.md)에 물리 주소로 보이는 메모리 주소를 [host](host.md)의 물리 주소로 변환할 수 있다. 이는 주소 변환의 두 번째 단계다. page table은 메모리 영역이 어디에 매핑되는지, 어떤 종류의 접근을 허용하는지 기록한다.

## 예시

앱이 가상 주소에서 데이터를 읽는다. guest의 page table은 이 주소를 guest 물리 주소로 매핑한다. 그런 다음 CPU는 EPT를 사용해 그에 대응하는 host 물리 주소를 찾는다. guest kernel은 자체 page table을 변경할 수 있지만 EPT는 제어하지 않는다. 다른 guest는 동일한 guest 물리 주소를 사용하더라도 같은 host 메모리를 사용하지 않을 수 있다.

## 두 번째 매핑은 누가 제어하는가?

[KVM](kernel-based-virtual-machine.md)을 사용하는 Linux host에서는 KVM이 두 번째 매핑을 설정한다. guest가 실행되는 동안 CPU는 이 매핑의 접근 권한을 적용한다. KVM이 지원하는 주소 변환은 [KVM 메모리 문서](https://docs.kernel.org/virt/kvm/x86/mmu.html#translation)를 참조한다.

[용어집으로 돌아가기](../glossary.md)
