# MicroVM

MicroVM は、通常の汎用 VM より仮想デバイスを減らすなどして、起動と実行に必要な処理やリソースを抑えるよう設計された [virtual machine](virtual-machine.md) です。独自のオペレーティングシステムの [kernel](kernel.md) を実行する点は変わりません。この名前が特定の起動時間やセキュリティ水準を保証するわけではありません。

## 例

あるテストサービスは、ジョブごとに仮想ディスクとネットワーク接続を備えた Linux microVM を割り当てますが、画面表示用のデバイスは提供しません。ジョブは普段使うコマンドラインツールを実行できます。MicroVM が公開していないデバイスを必要とする workload には、別の設定か実行環境が必要です。

## 仮想デバイスを減らすと何が変わるか

MicroVM 用の [virtual machine monitor](virtual-machine-monitor.md) は、対象の workload が必要としないデバイスを省けます。たとえば [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/README.md) は、不要なデバイスと guest 向けの機能を省き、オーバーヘッドと guest が到達できるコードを減らしています。提供するデバイスを絞ると、別のハードウェアを前提とする workload には対応しにくくなります。

[Isolation unit](isolation-unit.md) はサービスによって異なります。MicroVM には 1 つのジョブだけを入れることも、複数の workload を入れることもできます。同じ microVM 内の workload は guest kernel を共有します。また、sandbox がどの host ファイルとネットワークサービスを公開するかも確認してください。VM の規模が小さいからといって、許可されるアクセスが決まるわけではありません。

[用語集に戻る](index.md)
