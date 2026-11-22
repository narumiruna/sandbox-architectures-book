# MicroVM

[MicroVM](../../glossary/microvm.md) は、汎用の [virtual machine (VM)](../../glossary/virtual-machine.md) よりも実行時のオーバーヘッドを抑えるよう設計された VM です。通常、仮想デバイスの種類は少なくなりますが、独自の OS [kernel](../../glossary/kernel.md) を実行します。ジョブに専用の kernel が必要で、提供されるデバイスで足りる場合に選びます。「Micro」という名前だけでは、ジョブの起動にかかる時間やメモリ使用量は分かりません。

## ファイルを開く要求はどこに届くか {#where-the-file-request-goes}

1. [Lamp](../../practice/design/from-issue-to-patch.md) のテストランナーが `total.c` を開こうとします。Linux の [guest kernel](../../glossary/guest.md) がその [system call](../../glossary/system-call.md) を処理します。[host](../../glossary/host.md) の kernel が処理するわけではありません。
2. guest kernel は自身のファイルシステムでそのパスを探します。ファイルが仮想ディスク上にあれば、必要に応じてそのデバイスから読み取ります。
3. [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#host-integration) では、host 上のファイルを仮想ディスクの実体にできます。このデバイスを通して guest に見えるのは、仮想ディスクであり、host のファイルシステムではありません。

[virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md) である Firecracker は、仮想デバイスを提供し、[KVM を使って guest の CPU を実行します](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#internal-architecture)。Firecracker の[デバイスモデル](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#machine-model)には、仮想ストレージと仮想ネットワークが含まれますが、画面表示用のデバイスはありません。すべての microVM が同じデバイスを公開するとは限らないため、使う VMM を確認してください。

## 何を共有し、何を残すか決める {#decide-what-to-share-and-keep}

- **Kernel:** 同じ microVM 内の process は guest kernel を共有します。ジョブ間で kernel を共有してはいけない場合は、1 台に複数のジョブをまとめず、ジョブごとに microVM を割り当てます。
- **状態:** [cold boot](../../glossary/cold-boot.md) と [snapshot](../../glossary/snapshot.md) からの復元の両方が使える場合は、両者を比較します。たとえば、[Firecracker v1.11.0 の snapshot](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/snapshotting/snapshot-support.md#overview) は、guest のメモリとエミュレートしたハードウェアの状態を保存します。仮想ディスクの実体は運用者が別に管理します。再利用する前に、snapshot とディスクの両方にジョブのデータが残っていないか確認してください。
- **アクセス:** kernel を分けるだけでは、書き込み可能な共有ディレクトリを guest から隠したり、外部への通信を遮断したりすることはできません。ファイル、ネットワークの接続先、credentials へのアクセスルールを設定し、[検証してください](../../practice/verification/verifying-access-rules.md)。

ジョブに専用の Linux kernel が不要なら、[MicroVM vs gVisor](microvm-vs-gvisor.md) で両者を比較してください。
