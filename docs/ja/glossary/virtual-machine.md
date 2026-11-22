# Virtual machine (VM)

virtual machine（VM）は、自身の OS に仮想プロセッサ、メモリ、デバイスを提供するコンピューター環境です。その OS は独自の [guest kernel](guest.md) を持ちます。ハードウェア支援型の VM は、プロセッサの機能で guest の実行を [host](host.md) から分離しますが、sandbox は選んだ host リソースへのアクセスを guest に許可できます。

## 例

ビルドサービスは二つのジョブを別々の Linux VM で実行します。各ジョブは自身の guest ファイルシステムにパッケージをインストールできます。両方の VM に同じ host ディレクトリの書き込み可能な [mount](mount.md) を提供すると、各ジョブがそこで他方の使うファイルに影響を与えられます。

## VM が分離するもの

VM 内のプログラムは、ファイルを開くなどの機能を guest kernel に要求します。[hypervisor](hypervisor.md) は基盤の CPU とメモリの使用を制御し、[virtual machine monitor](virtual-machine-monitor.md) は VM と仮想デバイスを管理します。host kernel 上で process を動かす場合との違いは「[Sandbox isolation boundaries](../sandbox-isolation-boundaries.md#1-hardware-backed-virtual-machines)」を参照してください。

VM は一つの workload を実行することも、複数の [containers](container.md) を収容することもできます。各 container は別々のファイルシステムを持ちながら guest kernel を共有できます。何に専用の VM が割り当てられ、外側の sandbox がどのディスク、mount、ネットワーク接続を公開するかを確認してください。

[用語集に戻る](index.md)
