# ハードウェア支援型の VM {#hardware-backed-virtual-machines}

[virtual machine (VM)](../../glossary/virtual-machine.md) を使うと、[agent](../../glossary/agent.md) は独自の OS [kernel](../../glossary/kernel.md) を備えたコンピューター環境で作業できます。VM 内のプログラムは、OS への要求を [host](../../glossary/host.md) の kernel に直接送りません。

## 要求を処理するのは誰ですか？ {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md) のテストランナーが `total.c` を開くために [system call](../../glossary/system-call.md) を実行すると、[guest kernel](../../glossary/guest.md) がその要求を処理します。kernel は guest のファイルシステム内でそのパスを探します。プロジェクトが仮想ディスクや共有ディレクトリにあれば、guest はそこからプロジェクトを読み取れます。通常の Linux コマンドを実行できるからといって、host 上の任意のファイルを開けるわけではありません。

[virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md) は VM と、guest から見えるデバイスを管理します。たとえば、[リビジョン `58cf1b2c` の Firecracker](https://github.com/firecracker-microvm/firecracker/blob/58cf1b2cdca407f2323d1b0b25ebb95dfe5b4bcb/docs/design.md) は、Linux の guest に仮想ディスクと仮想ネットワークデバイスを提供します。[microVM](../../glossary/microvm.md) は一般に、汎用 VM よりも公開するデバイスが少ない一方、guest kernel は引き続き備えています。隔離境界とトレードオフを並べて確認するには、[VM、container、microVM の比較](../../sandbox-isolation-boundaries.md#compare-a-vm-a-container-and-a-microvm)を参照してください。

## 何が共有されますか？ {#what-stays-shared}

同じ VM 内の二つの [containers](../../glossary/container.md) は、VM の guest kernel を共有します。[pod](../../glossary/pod.md) ごとに VM を用意することと、container ごとに VM を用意することは同じではありません。一つの host 上の VM はそれぞれ独自の guest kernel を実行しますが、物理ハードウェアを共有することはあります。アーキテクチャの概説で、[どの処理が guest kernel を共有するか](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)を比較してください。

## 適した場面 {#when-to-use-it}

agent に完全な Linux [workspace](../../glossary/workspace.md) が必要で、なおかつ実行する処理に専用の kernel が必要なときは、この境界を選びます。たとえば、ネイティブのビルドや一連のテストを、host kernel 上で process を直接動かさずに実行できます。

## この境界では制限できないこと {#what-the-boundary-does-not-cover}

guest は、host が公開することを選んだファイルを利用できます。プロジェクトの共有ディレクトリが書き込み可能なら、guest はその中にある host のファイルを変更できます。guest がストレージやネットワーク経由で何にアクセスできるか確認してください。[snapshot](../../glossary/snapshot.md) を再利用する場合は、共有する前に、ディスクのデータとメモリの内容のどちらが含まれるか、あるいは両方が含まれるかを確認してください。

VMM と、それを利用する sandbox 製品については、[アーキテクチャの概説](../../agent-sandbox-architectures.md#hardware-backed-linux-environments)を参照してください。

仮想デバイスを絞った VM の仕組みと選び方については、[MicroVM](microvm.md) を参照してください。
