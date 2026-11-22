# Windows Hypervisor Platform (WHP)

Windows Hypervisor Platform（WHP）は、[virtual machine monitor (VMM)](virtual-machine-monitor.md) が host のハードウェア仮想化支援を使うための Windows のプログラミングインターフェースです。WHP は [host](host.md) 側のインターフェースであり、VMM、基盤の [hypervisor](hypervisor.md)、VM 内で動く kernel のいずれでもありません。

## 例

テストサービスは Windows 上で NVX を使って Linux の [microVM](microvm.md) sandbox を実行します。host 側の VMM は WHP を使って VM を動かします。sandbox 内のテストプログラムがファイルを開いたりプログラムを起動したりする際の要求先は、Windows API ではなく Linux の [guest kernel](guest.md) です。

## Windows のインターフェースが提供するもの

[Microsoft WHP API](https://learn.microsoft.com/en-us/virtualization/api/) を使うと、host のプログラムは guest を隔離する環境である *partition* を作成し、そのメモリを設定し、仮想プロセッサを作成して実行できます。「[API の定義](https://learn.microsoft.com/en-us/virtualization/api/hypervisor-platform/hypervisor-platform)」には、これらの操作と、呼び出し元がプラットフォームの機能を確認する方法が記載されています。VM の設定とデバイスの動作は引き続き VMM が提供します。

たとえば [リビジョン `42f413d` の NVX の Windows/WHP 要件](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#windows--whp)では、host のファームウェアでハードウェア仮想化を有効にし、Windows で Windows Hypervisor Platform 機能を有効にしてから再起動する必要があります。この API を Linux の host インターフェースである [KVM](kernel-based-virtual-machine.md) や [MSHV](microsoft-hypervisor.md) と混同しないでください。

[用語集に戻る](index.md)
