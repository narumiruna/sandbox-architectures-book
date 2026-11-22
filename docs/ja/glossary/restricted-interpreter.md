# Restricted interpreter

restricted interpreter は、自身が実装する言語機能と組み込み操作だけを使ってコードを実行します。コードが interpreter の外部にアクセスするには、[host](host.md) が提供する操作を使う必要があります。言語の機能が少なくても、権限が小さいとは限りません。host の操作が一つでも、広いアクセス権を与えることがあります。

## 例

あるビルドサービスでは、スクリプトがリスト、ループ、および承認済みビルドの結果を読む [tool](tool.md) を使って、失敗したテストを数えます。スクリプトは任意のファイルを開いたり、コマンドを起動したりできません。サービスは、tool が結果を返す前に、呼び出し元が指定のビルドの結果を読めるかを確認します。

## 対応する言語とライブラリ

interpreter は独自の規則に従ってスクリプトを評価します。restricted interpreter は、構文、組み込み操作、ライブラリへの対応の一部を省くことができます。見た目が JavaScript でも、一般的な JavaScript 環境と同じパッケージや操作に対応しているとは限りません。この方式に [WebAssembly](webassembly.md) や [engine isolate](engine-isolate.md) は必要ありません。

たとえば、[リビジョン `5310e422` の OpenCode Code Mode](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md) は、Psychoscript を使って JavaScript に似た言語を解釈します。このリビジョンでは、パッケージを読み込まず、スクリプトにファイルシステム、ネットワーク、process への直接アクセスを許可しません。interpreter の外部での作業には、host が tool を提供します。

## 言語の制限だけでは足りないこと

対応しているループでも実行に時間がかかりすぎる場合があり、承認済みの tool 呼び出しでも想定より多くのデータを返す場合があります。実行時間、メモリ、tool の使用は個別に制限してください。各 tool には [least privilege](least-privilege.md) を適用します。テスト結果を読む tool に、任意のコマンドを実行する手段まで持たせるべきではありません。

[用語集に戻る](index.md)
