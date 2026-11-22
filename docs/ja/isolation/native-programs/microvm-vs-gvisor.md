# MicroVM vs gVisor

まず、**ジョブに専用の Linux kernel が必要か**を確認します。必要なら、要件を満たす guest kernel とデバイスを備えた [MicroVM](microvm.md) から検討します。不要なら、[gVisor](gvisor.md) も候補になります。ただし、対象の Linux [container](../../glossary/container.md) が gVisor で動作することが条件です。MicroVM は [virtual machine](../../glossary/virtual-machine.md) の一種で、gVisor は [user-space kernel](../../glossary/user-space-kernel.md) の実装の一つです。名前だけでは、実際の環境でどちらが安全か、速いかは分かりません。

## 実行境界を比較する {#compare-the-execution-boundaries}

プログラムがファイルを開こうとしたときの主な違いは、[どのコンポーネントが要求を処理するか](../../sandbox-isolation-boundaries.md#sandboxes-for-operating-system-workloads)です。設定次第で、どちらの境界でも同じプロジェクトファイルを公開できます。

| 確認すること | MicroVM | gVisor |
| --- | --- | --- |
| Linux の [system call](../../glossary/system-call.md) を処理するのは何か？ | VM 内で動作する Linux の [guest kernel](../../glossary/guest.md)。 | KVM プラットフォームを使う場合も、[Sentry](https://gvisor.dev/docs/architecture_guide/intro/#how-does-gvisor-provide-isolation)。 |
| [host](../../glossary/host.md) に何が必要か？ | ハードウェア支援型の microVM では、対応する仮想化バックエンド。たとえば、[Firecracker v1.11.0 は KVM を使います](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#internal-architecture)。 | 対応する Linux host。[systrap はハードウェア支援による仮想化を必要としません](https://gvisor.dev/docs/architecture_guide/intro/#how-does-gvisor-provide-isolation)が、[KVM プラットフォームはそれを使います](https://gvisor.dev/docs/architecture_guide/platforms/#kvm)。 |
| ジョブは何を利用できるか？ | 選んだ guest kernel のインターフェースと、VM が公開するデバイス。 | [gVisor が実装する Linux のインターフェース](https://gvisor.dev/docs/user_guide/compatibility/)と、runtime が公開するリソース。 |
| どのジョブが同じ境界を共有するか？ | 同じ microVM に割り当てられたジョブは guest kernel を共有します。 | 同じ gVisor sandbox に割り当てられたジョブは Sentry を共有します。 |

## 実際のジョブを一つ使って選ぶ {#make-the-choice-with-one-real-job}

1. **必須要件を確認する。** テストで特定の Linux kernel ビルドの動作を検証するなら、そのビルドを起動できる microVM を使います。container image から user space のプログラムをコンパイルしてテストするだけなら、gVisor も試してください。基本的な動作確認だけでは不十分です。インストール、ビルド、テストを一通り実行してください。
2. **両方で同じアクセスルールを確認する。** 同じリビジョンのプロジェクトを使い、各ジョブには意図したファイル、ネットワークの接続先、credentials だけを利用できるようにします。どのジョブが同じ sandbox を共有し、何が次の実行に引き継がれるかを確認してください。これらは、表で比較した仕組みとは別に決めることです。
3. **要件を満たす候補だけを計測する。** runtime のバージョンとプラットフォームに加え、環境を新規に起動するのか、保存した状態を復元するのか、準備済みの sandbox を割り当てるのかを記録します。最初のコマンドを実行できるまでの時間、ジョブの完了までの時間、想定した同時実行数での host のメモリ使用量を[計測してください](../../practice/verification/measuring-a-sandbox.md)。一方を新規に起動し、他方では準備済みの worker を使うと、計測結果の差を隔離方式だけで説明することはできません。

両方の選択肢を備えたシステムの例については、[Agent Substrate のアーキテクチャ](../../agent-substrate.md)を参照してください。
