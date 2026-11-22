# Engine isolate {#engine-isolates}

[engine isolate](../../glossary/engine-isolate.md) は、[V8](https://github.com/v8/v8/blob/13.8.258/include/v8-isolate.h#L277-L285) などの言語エンジンの中で、スクリプトのオブジェクトと実行状態をほかのスクリプトから分離します。コードが利用できる API は、エンジンを組み込むプラットフォームが決めます。

## 要求を処理するのは誰ですか？ {#who-handles-the-request}

スクリプトが [`LAMP-17`](../../practice/design/from-issue-to-patch.md) のタイトルを要求すると、エンジンがスクリプトを実行し、プラットフォームが名前付きの接続を通じてその要求を issue サービスに送ります。issue サービスは、その issue に対する [authorization](../../glossary/authorization.md) を確認してから、タイトルを返します。

[Cloudflare Dynamic Workers](https://blog.cloudflare.com/dynamic-workers/) は、この種の実行環境を JavaScript 向けに提供します。Cloudflare のドキュメントにある例では、呼び出し側が `globalOutbound: null` を設定して通常の外向きの要求をブロックしても、別のサービスへの名前付き接続である特定の **binding** は提供できます。

## 何が共有されますか？ {#what-stays-shared}

エンジンは各スクリプトの状態を分離しますが、複数の isolate が同じ OS の [process](../../glossary/process.md) を共有することはあります。プラットフォームは、複数の isolate を同じサービスに接続することもできます。isolate は独立した process や [VM](../../glossary/virtual-machine.md) ではありません。

## 適した場面 {#when-to-use-it}

スクリプトに言語エンジンの機能と少数のプラットフォーム API が必要で、シェルやネイティブパッケージは不要なときは、この境界を選びます。

## この境界では制限できないこと {#what-the-boundary-does-not-cover}

スクリプトが直接ネットワークに要求を送れなくても、任意の URL からデータを取得できる binding があれば、広いアクセス権を与えることになります。worker の binding と既定のネットワークアクセスは、あわせて確認してください。また、どのスクリプトが process を共有するか、プラットフォームがエンジンの周りにどのような制御を設けているかも確認してください。
