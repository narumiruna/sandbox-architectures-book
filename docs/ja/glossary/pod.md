# Pod

Pod は、Kubernetes がデプロイできる最小単位です。1 つ以上の [container](container.md) が一緒に動き、ネットワーク環境を共有し、ストレージも共有できます。Pod に専用の kernel があるとは限りません。[Isolation boundary](isolation-boundary.md) は選んだ runtime で決まります。

## 例

あるテスト用 sandbox は、Web サーバーとテストランナーを同じ pod 内の 2 つの container で実行します。テストランナーは `localhost` でサーバーに接続できます。サービスが両方の container に共有の出力ディレクトリを mount すれば、どちらもそこに保存されたテスト結果を読み取れます。

## Pod を共有するとは

[Kubernetes の Pods ドキュメント](https://kubernetes.io/docs/concepts/workloads/pods/) が説明する標準モデルでは、pod 内の container は IP アドレスとポート空間を共有します。ストレージを共有するには、必要とする container 向けに設定が必要です。[Virtual machine](virtual-machine.md) を使う runtime では、pod を [isolation unit](isolation-unit.md) にできます。たとえば [Kata Containers 4.4.0](https://github.com/kata-containers/kata-containers/blob/4.4.0/docs/design/architecture/README.md#kubernetes-support) は Kubernetes の pod を VM 内に配置します。Pod 内の container はその VM の guest kernel を共有し、container ごとに別の VM が割り当てられるわけではありません。Container ごとに VM を割り当てる場合との違いは、[guest kernel を共有する workload](../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel) を参照してください。

[用語集に戻る](index.md)
