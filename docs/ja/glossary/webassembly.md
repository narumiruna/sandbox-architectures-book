# WebAssembly (Wasm)

WebAssembly（略称 Wasm）は、実行可能なコードを異なる環境に持ち運べる形式です。Wasm [runtime](runtime.md) は、コードに必要な機能を備えていれば、異なるプロセッサや OS で同じコードを実行できます。Wasm 自体はファイルシステム、ネットワーク接続、シェルを提供しません。コードがアクセスできるものは [host](host.md) が何を提供するかで決まります。

## 例

ログサービスは、警告を数えるために、命令とデータをまとめた Wasm module を実行します。host がログのテキストを渡し、module は件数を返します。module 自体がログファイルを開く必要はないため、サービスはファイルシステムへのアクセスを許可しません。

## メモリと import

runtime が module の実行可能なインスタンスを作る際には、module が外部から必要と宣言した関数などのリソースである *import* を接続します。[WebAssembly Core Specification 1.0](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#imports) は、関数やメモリを含められる import を定義しています。Wasm は、インスタンスが使えるバイト範囲である *linear memory* を読み書きします。[その範囲外へのアクセス](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#memory-instructions)は、host process の別のメモリに届く代わりに、エラーで実行を停止します。

runtime のメモリチェックは [host function](host-function.md) の影響を制限しません。ファイルを読む関数は、呼び出し元がファイルを直接読めない場合でも、独自のアクセス規則を適用する必要があります。host は、独自の関数や [WebAssembly System Interface (WASI)](webassembly-system-interface.md) のような標準インターフェースを提供できます。別の場所で module を実行するには、新しい環境が必要な Wasm 機能と import に対応しているか確認してください。

## 何を Wasm にコンパイルするのか

workload 自体が Wasm module の場合もあれば、module が workload を動かす言語エンジンの場合もあります。[リビジョン `9c465268` の Pi `codemode`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) は、QuickJS を Wasm にコンパイルし、実行する JavaScript に tool を提供します。エンジンが Wasm module であり、スクリプトは JavaScript のままです。依存関係の名前が [`quickjs-wasi`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/package.json) でも、スクリプトに何へのアクセスが許可されるかはわかりません。

## 使用に適した場面

完全な OS がなくても、選んだ host の操作だけで動くコードには Wasm を検討してください。通常の Linux の [native binary](native-binary.md) は Wasm module として直接実行できません。tool による検索の例は「[基礎編の WebAssembly](../isolation/generated-scripts/webassembly.md)」を参照してください。

[用語集に戻る](../glossary.md)
