# Container

Container は、一つ以上のプログラムを実行するために用意した環境です。プログラムにファイルシステムと、作業に使う一式のリソースを提供します。*Container* という言葉だけでは、プログラムを Host から何が隔てているかは分かりません。

## 例

コードレビューサービスが、プロジェクトで必要なコンパイラーとテストツールを備えた Container を起動します。二つ目のテストジョブは、同じ [container image](container-image.md) から別の Container を起動できます。イメージは開始時のファイルを提供します。実行中の Container には、それぞれ独自のテスト用 Process があり、別々の書き込み可能なファイルシステムを持つこともあります。

## 隔離を担う仕組み

[container runtime](container-runtime.md) が環境を準備します。Kernel を共有する構成では、Linux の [namespace](namespace.md) で Process ごとに異なる範囲のリソースを見せ、[control group](control-group.md) でリソース使用量を集計または制限できます。Runtime は、Container を [user-space kernel](user-space-kernel.md) を介して実行したり、[virtual machine](virtual-machine.md) の中で実行したりすることもできます。どの方式も同じイメージから開始できますが、[isolation boundary](isolation-boundary.md) は異なります。

Runtime が Workload と何を共有するかを確認してください。たとえば、書き込み可能な Host の [mount](mount.md) があると、Container のパッケージ化の方法にかかわらず、コードが Host 上のファイルを変更できることがあります。[VM、Container、MicroVM の比較](../sandbox-isolation-boundaries.md#compare-a-vm-a-container-and-a-microvm)を参照してください。

[用語集に戻る](index.md)
