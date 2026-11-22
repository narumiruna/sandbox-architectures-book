# Code Mode

Code Mode は、モデルがツールを呼び出して結果をまとめるプログラムを書く方式です。この用語はモデルによるツールの使い方を指し、プログラムをシステムの他の部分から分離する仕組みを指すものではありません。プログラムが Sandbox 内で実行されても、ツールハンドラーや Agent の他の部分はその外で動く場合があります。

## 例

[agent](agent.md) が、未解決の Issue があるマイルストーンの一覧を必要としています。Issue の検索を一件ずつモデルに求める代わりに、生成した一つのスクリプトを [sandbox](sandbox.md) で実行します。スクリプトはマイルストーンごとに Issue を検索するツールを呼び出し、結果を数えて短い要約を返します。Agent は次の判断にその要約を使えます。

## 生成したプログラムの実行

アプリケーションは、スクリプトが呼び出せるツールと、スクリプトを実行する [runtime](runtime.md) を選びます。たとえば、[本書が扱うリビジョンの Pi `codemode`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) は、[WebAssembly](webassembly.md) にコンパイルした QuickJS 内で JavaScript を実行し、アプリケーションが提供するツールを公開します。[restricted interpreter](restricted-interpreter.md) を使えば、Wasm なしでも Code Mode を実行できます。

## ツール呼び出しの確認

スクリプトを囲む境界は、スクリプトが利用できるツールを制限できます。それでも各 [tool](tool.md) のハンドラーは、要求された操作が許されているか確認する必要があります。スクリプトに直接のネットワークアクセスがなくても、Issue の検索ではプロジェクトを確認する必要があります。他の実装については[アーキテクチャの概観（英語）](../../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells)を参照してください。

[用語集に戻る](../glossary.md)
