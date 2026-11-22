# WebAssembly System Interface (WASI)

[WebAssembly System Interface (WASI)](https://wasi.dev/) は、ファイルの読み取りや時刻の確認などの作業のために、host が [WebAssembly](webassembly.md) プログラムに提供できる標準インターフェース群です。WASI はこれらのサービスの要求方法を定めます。OS ではなく、インターフェースに対応するだけで、それが扱えるすべてのリソースへのアクセスが許可されるわけでもありません。

## 例

sandbox は WASI を通じて、テスト結果のディレクトリへの読み取り専用アクセスをレポート生成プログラムに与えます。プログラムは host のファイルシステム全体を渡されなくても結果を読めます。与えられたアクセスは読み取り専用なので、そのディレクトリには書き込めません。

## インターフェースと権限

Wasm プログラムは、必要なインターフェースを import として宣言します。import は、プログラムの外部から提供される必要がある関数やリソースへの要求です。host は、それらのインターフェースを通じて何へのアクセスを許可するかを選びます。たとえば WASI 0.2.0 の [ファイルシステムの preopens インターフェース](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/filesystem/preopens.wit)は、起動時にプログラムにアクセスが許可されたディレクトリを列挙します。[ファイルシステムの型定義](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/filesystem/types.wit)では、ファイルシステムへの要求に使う参照である *handle* が示すディレクトリの内側に、パスが収まることを要求します。アクセスフラグは、その handle を通じた変更を防げます。

インターフェース名だけでなく、実際に許可されたアクセスを確認してください。プログラムは WASI 外へのアクセスを提供する独自の [host functions](host-function.md) を受け取ることもあります。それらの関数には独自の権限チェックが必要です。

## バージョンと OS の互換性

[WASI Preview 1](https://wasi.dev/releases/wasi-p1) は、`wasi_snapshot_preview1` という名前の core Wasm module の import を使います。[WASI 0.2 (Preview 2)](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/README.md) は WebAssembly Component Model を使います。これは、関数名やデータ型を記述する言語である WIT で定義されたインターフェースを介して、Wasm component を接続する仕組みです。プログラムが期待するバージョンとインターフェースを、[runtime](runtime.md) と host が提供するものと照合してください。WASI は Linux kernel を提供せず、通常の Linux の [native binary](native-binary.md) を Wasm として実行できるようにするものでもありません。

[用語集に戻る](../glossary.md)
