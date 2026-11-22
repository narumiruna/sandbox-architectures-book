# Artifact

Artifact は、パッチ、テストレポート、ビルド結果など、ジョブの終了後にシステムが選んで保存する出力です。[workspace](workspace.md) 全体を指すわけではありません。

Lamp のタスクでは、収集コンポーネントがレビュー用にテキストのパッチとテスト出力を受け取ります。実行に使った Worker はすぐに破棄できます。レビュー用の保存先には、保持期間が終わるまでそのファイルが残ります。レビュー担当者はどちらも信頼できない出力として扱い、読むには権限が必要です。

[Workspace と Artifact（英語）](../../practice/data-and-access/workspaces-and-artifacts.md)を参照してください。
