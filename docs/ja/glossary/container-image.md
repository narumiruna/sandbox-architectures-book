# Container image

Container image は、[container runtime](container-runtime.md) が [container](container.md) を起動するために使うファイルと設定をまとめたものです。プログラムの実行中の状態ではなく、開始時の環境を記述します。

## 例

ビルドサービスは、Python インタープリターとプロジェクトの依存関係を含む一つのイメージを再利用できます。新しい Container はどれも同じファイルで開始できます。あるビルドが書き出したレポートは元のイメージには含まれません。サービスが別途保存または共有しない限り、別のビルドでは見えません。

## パッケージの内容

[OCI Image Format v1.1.0](https://github.com/opencontainers/image-spec/blob/v1.1.0/manifest.md) は、設定とファイルシステムのレイヤーを参照する *manifest* によってイメージを記述します。設定には、実行するコマンドなどの既定値を指定できます。各レイヤーにはファイルシステムへの変更が記述されており、イメージを扱うツールが順に適用して、Container の開始時のファイルを用意します。

イメージは、メモリーの [snapshot](snapshot.md) のように実行中の Process を保存するものでも、Workload の隔離方法を決めるものでもありません。互換性があれば、同じイメージを異なる Runtime で実行できます。コードから何にアクセスできるかは、Runtime とその Policy を確認します。

[用語集に戻る](../glossary.md)
