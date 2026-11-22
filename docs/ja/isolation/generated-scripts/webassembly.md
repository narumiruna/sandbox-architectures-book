# WebAssembly {#webassembly}

[WebAssembly (Wasm)](../../glossary/webassembly.md) を使うと、[host](../../glossary/host.md) アプリケーションは、メモリへのアクセスを検査し、外部で呼び出せる操作を定めた上で、モジュールを実行できます。モジュールを実行するだけで、シェル、ファイルシステム、ネットワーク接続が使えるようになるわけではありません。

## 要求を処理するのは誰ですか？ {#who-handles-the-request}

プログラムが [`LAMP-17`](../../practice/design/from-issue-to-patch.md) のタイトルを要求すると、Wasm [runtime](../../glossary/runtime.md) は、アプリケーションが issue の検索用に用意した [host function](../../glossary/host-function.md) をモジュールが呼び出せるようにします。host function は、その issue に対する [authorization](../../glossary/authorization.md) を確認してから、タイトルを返します。タイトルの並べ替えはモジュール内で実行できます。

この境界の内側で生成コードを実行する方法には、よく使われる二つの設計があります。

1. **処理を Wasm モジュールとして実行します。** アプリケーションは処理を Wasm にコンパイルし、[Wasmtime](https://docs.wasmtime.dev/security.html) などの runtime で実行できます。モジュールは、アプリケーションが提供する host 側の操作を呼び出せます。
2. **言語エンジンを Wasm モジュールとして実行します。** [リビジョン `9c465268` の Pi](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) では、QuickJS を Wasm にコンパイルしています。モデルが書くコードは引き続き JavaScript で、QuickJS がそれを解釈して実行します。

## 何が共有されますか？ {#what-stays-shared}

複数のモジュールを同じ host [process](../../glossary/process.md) で実行できますが、既定では互いのメモリにアクセスできません。host は、issue の検索サービスなど、同じリソースを複数のモジュールへ明示的に提供できます。

## 適した場面 {#when-to-use-it}

実行する処理またはその言語エンジンが Wasm で動作し、通常の Linux [binaries](../../glossary/native-binary.md) を必要としないときは、この境界を選びます。

## この境界では制限できないこと {#what-the-boundary-does-not-cover}

メモリを検査しても、host function がモジュールの代わりに行う操作は制限されません。[WebAssembly System Interface (WASI)](../../glossary/webassembly-system-interface.md) が host のファイルシステムへのアクセスを許可すると決めつけず、アプリケーションがどの操作を提供しているかを確認してください。また、runtime がメモリの使用量をどう制限し、実行時間が長すぎるプログラムをどう停止するかも確認してください。

tool を呼び出すスクリプトを実行する他の方法については、[アーキテクチャの概説](../../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells)を参照してください。
