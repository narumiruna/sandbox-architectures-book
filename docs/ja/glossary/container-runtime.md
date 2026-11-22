# Container runtime

Container runtime は、[container](container.md) を準備して実行するソフトウェアです。選択された隔離設定を適用し、プログラムを起動します。二つの Runtime が同じ [container image](container-image.md) から起動しても、プログラムを囲む境界は異なる場合があります。

## 例

ビルドサービスが、テストジョブ用の Sandbox を起動するよう Runtime に頼みます。Runtime はプロジェクトを `/workspace` で利用できるようにし、テストランナーを起動します。ジョブをいつどこで実行するかはサービスが決め、ジョブを実行する環境は Runtime が準備します。

## パッケージ内のファイルから Process を起動するまで

Container のソフトウェア群は、イメージのファイルを展開して Runtime の設定と組み合わせ、Workload の起動に必要なローカルのファイルと設定をひとまとめにした *bundle* を用意できます。[OCI Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/tree/v1.2.1) は、bundle と、作成や起動などのライフサイクル操作を規定します。低レベルの Runtime は、自分でイメージをダウンロードせずに、準備済みの bundle を受け取れます。

## Kernel インターフェースの提供元

Runtime は、[namespace](namespace.md) を用いて [host kernel](kernel.md) を直接使うことも、[user-space kernel](user-space-kernel.md) を提供することも、独自の Kernel を持つ [virtual machine](virtual-machine.md) で Workload を実行することもできます。[control plane](control-plane.md) は Workload を管理します。Workload を Host から何で隔てるかは、Runtime の実行の仕組みと設定で決まります。

[用語集に戻る](../glossary.md)
