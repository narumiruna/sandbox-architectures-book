# Guest

Guest とは、[virtual machine](virtual-machine.md) 内で実行されるオペレーティングシステムとプログラムです。そのオペレーティングシステムの中核である *guest [kernel](kernel.md)* が、VM が提供するプロセッサー、メモリー、デバイスを管理します。Guest のオペレーティングシステムと Kernel は、[host](host.md) 側のものとは別です。

## 例

Sandbox が Linux Guest 内でテストを実行します。テストがファイルを開くときは、物理的な Linux コンピューターと同じように Guest kernel に要求します。ファイルの置き場所が、Host 側のファイルを実体とする仮想ディスクであっても、Guest から見えるのはディスクであり、Host がその実体を保管するディレクトリーではありません。

## Guest が制御するもの

Guest 上のプログラムは [system call](system-call.md) で Guest kernel に要求を出します。Guest kernel は VM 内のプログラムとファイルを管理します。[hypervisor](hypervisor.md) と [virtual machine monitor](virtual-machine-monitor.md) は、仮想ハードウェアの提供に必要な役割を分担します。たとえば、[Firecracker v1.11.0 の設計](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md)では、Host 側のファイルを実体とする仮想ブロックデバイスを説明しています。

Guest 内の管理者が、自動的に Host の管理者権限を持つわけではありません。それでも、Guest に意図的に公開する Host 側のファイル、ネットワークサービス、その他のリソースには、それぞれアクセス制御が必要です。同じ VM にある Workload は Guest kernel を共有します。それらの Workload を分ける必要があるなら、[isolation unit](isolation-unit.md) を確認してください。

[用語集に戻る](../glossary.md)
