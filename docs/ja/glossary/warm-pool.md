# Warm pool

warm pool は、要求が届く前に準備しておく [sandboxes](sandbox.md) の集まりです。要求はすべてのセットアップを待たずに、その一つを確保できます。どこまで準備済みかはプラットフォームによって異なり、準備済みの sandbox でも要求ごとの設定が必要な場合があります。

## 例

ビルドサービスは、コンパイラをインストールしてコマンド実行サービスを起動済みの、未割り当ての Linux sandbox を三つ保持します。要求はその一つを確保し、プロジェクトのファイルを接続してビルドを始めます。三つとも確保済みなら、次の要求は待機するか、[cold start](cold-start.md) が必要になります。

## 保存ファイルではなく準備済みインスタンス

[control plane](control-plane.md) はインスタンスを準備し、要求に割り当て、プールを補充できます。たとえば [Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/examples/warmpool-quickstart/README.md) は、インスタンスを準備する `SandboxWarmPool` と、その一つを取得する `SandboxClaim` を説明しています。このライフサイクル管理の仕組みは、sandbox が workload をどう隔離するかを決めません。

[snapshot](snapshot.md) は保存済みの状態です。サービスは snapshot を復元して warm pool を補充できますが、snapshot だけを保持する場合、要求が届いてから復元する作業が残ります。プールは作業を前倒しする代わりに、待機中もリソースを確保します。未割り当てのインスタンスに [tenant](tenant.md) のデータを含めず、準備にかかる時間の測定には割り当てと workspace の設定も含めてください。

[用語集に戻る](../glossary.md)
