# Restricted interpreter {#restricted-interpreters}

[restricted interpreter](../../glossary/restricted-interpreter.md) で使えるのは、その interpreter が実装している言語機能と組み込みの操作だけです。それ以外にスクリプトが呼び出せる操作は、[host](../../glossary/host.md) が提供します。見慣れた言語名でも、普段使うライブラリやシステム API が利用できるとは限りません。

## 要求を処理するのは誰ですか？ {#who-handles-the-request}

スクリプトが [`LAMP-17`](../../practice/design/from-issue-to-patch.md) のタイトルを要求すると、interpreter はスクリプトを実行しますが、検索処理は host の [tool](../../glossary/tool.md) に任せます。tool は、その issue に対する [authorization](../../glossary/authorization.md) を確認してから、タイトルを返します。ループや並べ替えは interpreter 内で実行します。スクリプトに issue tracker のライブラリや直接のネットワークアクセスは不要です。

[リビジョン `5310e422` の OpenCode](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md) は、JavaScript の一部を扱うために Psychoscript を使います。[Pydantic AI Code Mode](https://pydantic.dev/docs/ai/harness/code-mode/) は、Python の一部を扱うために [Monty（リビジョン `5f4a3dfc`）](https://github.com/pydantic/monty/blob/5f4a3dfc493538bb9dc319974393391ba9e7cf14/README.md) を使います。どちらも、完全な言語環境を提供せずに、生成コードから tool を呼び出せるようにできます。

## 何が共有されますか？ {#what-stays-shared}

interpreter は、host アプリケーションの [process](../../glossary/process.md) 内で実行できます。言語機能を制限するだけでは、OS を分離したり、スクリプトごとに process を割り当てたりすることにはなりません。異なるスクリプトが同じ host の tool を使うこともできます。

## 適した場面 {#when-to-use-it}

スクリプトの主な役割が、複数の tool の呼び出しを組み合わせて結果を処理することなら、この境界を選びます。モデルが生成しそうなコードでテストしてください。短く正しい Python や JavaScript のコードでも、対応範囲外の機能やライブラリを使うことがあります。

## この境界では制限できないこと {#what-the-boundary-does-not-cover}

ファイルへ直接アクセスできないスクリプトでも、書き込み先を制限しない tool を呼び出せるなら、host のファイルを変更できます。host の tool は別途確認してください。また、サポートされているループでも実行時間が長くなりすぎることがあるため、interpreter が長時間動作するスクリプトをどう停止するかも確認してください。
