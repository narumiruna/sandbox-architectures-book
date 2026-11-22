# Kernel-based Virtual Machine (KVM)

Kernel-based Virtual Machine (KVM) は、プロセッサーの仮想化機能を使って [virtual machine](virtual-machine.md) を実行する Linux kernel の機能です。[Host](host.md) 上のソフトウェアに、VM を作成して実行するためのインターフェースを提供します。KVM は [guest kernel](guest.md) でも、VM とそのデバイスを管理するプログラム全体でもありません。

## 例

あるビルドサービスは、Linux host 上の [virtual machine monitor (VMM)](virtual-machine-monitor.md) を使って Linux sandbox を動かします。VMM は KVM を使って guest の仮想プロセッサーを実行し、ビルド用の仮想ディスクを提供します。ビルドツールは、host 上の KVM ではなく guest kernel に通常の Linux のリクエストを送ります。

## Host インターフェース

[Linux KVM API](https://docs.kernel.org/virt/kvm/api.html) は、VMM が `/dev/kvm` を開き、VM と仮想プロセッサーを作成し、guest のメモリーを設定する方法を説明しています。オプション機能への対応は host によって異なるため、VMM はどの機能が利用できるかを問い合わせることができます。

VMM には host 上の `/dev/kvm` へのアクセスが必要です。たとえば [リビジョン `42f413d` の NVX Linux/KVM 要件](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#linux--kvm) では、ハードウェア仮想化とデバイスへの読み書きアクセスが必要です。このアクセス権は host 側の VMM に必要なもので、sandbox 内の workload に与えるものではありません。ほかの host インターフェースについては [MSHV](microsoft-hypervisor.md) と [WHP](windows-hypervisor-platform.md) を参照してください。

[用語集に戻る](index.md)
