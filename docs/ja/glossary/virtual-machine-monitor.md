# Virtual machine monitor (VMM)

virtual machine monitor（VMM）は、[virtual machine](virtual-machine.md) を作成または管理し、仮想デバイスを提供するソフトウェアです。このソフトウェアを [hypervisor](hypervisor.md) と呼ぶプロジェクトもあります。本書では *VMM* は VM とデバイスの管理を指し、sandbox サービス全体や VM 内の OS は指しません。

## 例

テストサービスは VM を起動し、VMM に仮想ディスクの接続を要求します。VM 内のプログラムはファイルの読み取りを [guest kernel](guest.md) に要求します。VMM は仮想ディスクの動作を提供しますが、プログラムからの要求を guest の system call として直接受け取るわけではありません。

## host インターフェースと guest の間

ハードウェア支援型 VM では、VMM は host の仮想化インターフェースを介して guest メモリと仮想プロセッサを設定します。また guest に見える仮想デバイスを提供または接続します。たとえば [Firecracker v1.11.0 の設計文書](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md)は、[KVM](kernel-based-virtual-machine.md) を使って仮想プロセッサを動かし、host 上のファイルを裏付けとする仮想ディスクを提供する方法を説明しています。

sandbox の [control plane](control-plane.md) は VMM を使って VM を起動・停止できますが、ジョブをどこで実行するか、誰に workspace やネットワークへのアクセスを与えるかは別の責務です。公開されるものを知るには VMM だけでなく sandbox 全体を確認してください。

[用語集に戻る](index.md)
