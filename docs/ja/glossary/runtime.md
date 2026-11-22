# Runtime

runtime は、コードを実行するか、そのコードが動く環境を用意するソフトウェアです。この語だけでは、どんなコードを実行できるか、他のプログラムと何によって分離されるかはわかりません。

## 例

agent サービスは、[WebAssembly](webassembly.md) にコンパイルされたレポート生成プログラムを、テスト結果にアクセスできる sandbox で動かします。新しいテストを実行するときは、[container runtime](container-runtime.md) を介してビルド用の container を起動します。Wasm runtime はレポート生成プログラムを実行し、container runtime はネイティブのテストプログラムが動く環境を用意します。

## runtime が実行するもの、用意するもの

言語 runtime は、言語エンジンや [restricted interpreter](restricted-interpreter.md) を使ってスクリプトを実行できます。Wasm runtime は、Wasm の命令とデータをまとめた module を読み込んで実行します。runtime が module の実行可能なインスタンスを作る際、アプリケーションは選んだ [host functions](host-function.md) を提供できます。一方、container runtime は process のためにファイルシステムなどのリソースを用意します。たとえば、[OCI Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/blob/v1.2.1/runtime.md#lifecycle) は、プログラムの起動前に設定から container 環境を作る手順を説明しています。

## 管理と隔離は別の役割

[control plane](control-plane.md) は sandbox をいつどこで起動するかを決め、runtime はコードを実行するか、その環境を用意します。一つの製品が両方を担う場合もあります。[isolation boundary](isolation-boundary.md) を特定するには、何が分離を強制し、workload が host のどのリソースを使えるかを確認してください。たとえば、container runtime は、host kernel を共有する process を起動することも、別の kernel を持つ VM 内で process を動かすこともできます。

[用語集に戻る](index.md)
