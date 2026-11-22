# Microsoft Hypervisor (MSHV)

Microsoft Hypervisor は、guest のオペレーティングシステムが物理コンピューターをどのように使うかを制御するソフトウェアです。本書では、対応する Linux host 上で [virtual machine monitor (VMM)](virtual-machine-monitor.md) が `/dev/mshv` を通じて利用できる Microsoft Hypervisor の backend を *MSHV* と呼びます。このデバイスは host インターフェースであり、[guest kernel](guest.md) でも VMM 自体でもありません。

## 例

あるビルドサービスは NVX を使い、MSHV が有効な Linux host 上で Linux [microVM](microvm.md) の sandbox を実行します。Host 上の VMM は `/dev/mshv` を使って VM を実行します。VM 内でビルドツールがファイルを開いたりプログラムを実行したりするときは、guest 側の Linux kernel に依頼します。

## Linux インターフェースが使える環境

[Microsoft Hypervisor の仕様](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/tlfs) では、分離された実行環境を *partition* と呼びます。*Root partition* は、マシンを管理し、仮想化スタックを動かす特権付きの環境です。[リビジョン `42f413d` の NVX Linux/MSHV 要件](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#linux--mshv) では、MSHV が有効な kernel を使って root partition 内で Linux を動かす必要があります。その kernel は `/dev/mshv` を公開する必要があり、VMM には読み書きアクセスが必要です。Hypervisor 上の通常の Linux guest はこの要件を満たしません。

この Linux backend を、VMM が Windows 上で使える host API の [Windows Hypervisor Platform (WHP)](windows-hypervisor-platform.md) や、別の Linux host インターフェースである [KVM](kernel-based-virtual-machine.md) と混同しないでください。

[用語集に戻る](index.md)
