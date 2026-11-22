# Isolation unit

Isolation unit は、同じ isolation boundary の内側で実行される workload のまとまりです。ある層の境界は、ある unit を別の unit から分離しますが、同じ unit 内の workload までは分離しません。

## 例

あるサービスでは Kubernetes の [pod](pod.md) ごとに、sandbox として専用の [virtual machine](virtual-machine.md) を割り当てます。ある pod には、テストランナーと結果を収集する補助プログラムが入っています。両者は同じ VM とそのオペレーティングシステムの kernel を共有します。別の pod には別の VM が割り当てられます。したがって、VM の境界が分離するのは pod 同士であり、最初の pod 内の 2 つのプログラムではありません。

## Unit が示す層

[Isolation boundary](isolation-boundary.md) は作業を*どう分離するか*を示します。Unit は個々の境界が*どの作業をひとまとめにするか*を示します。Pod ごとに VM を割り当てるなら unit は pod、container ごとなら [container](container.md) です。[Guest kernel を共有する workload（英語）](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel) の図では、3 つの実装を比較しています。

同じシステムでも、別の層にはより小さな unit があり得ます。1 台の VM 内の process がそれぞれ異なるファイルシステムを見ていても、process ごとに別の guest kernel があるわけではありません。2 つの [tenant](tenant.md) が guest kernel を共有してはいけない場合は、VM の有無だけでなく、[control plane](control-plane.md) がそれらの workload をどう配置するかを確認します。

[用語集に戻る](../glossary.md)
