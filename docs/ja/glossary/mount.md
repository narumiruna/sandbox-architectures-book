# Mount

ファイルシステムやディレクトリを mount するとは、その中のファイルをあるパスから見えるようにすることです。*Bind mount* は、既存のファイルやディレクトリをコピーせずに別のパスから見えるようにします。Sandbox が bind mount 経由で書き込める場合は、元のファイルを変更できます。

## 例

コードレビュー用の sandbox では、host のプロジェクトディレクトリが `/workspace` に見えます。サービスはそのディレクトリを読み取り専用で mount します。レビュープログラムはプロジェクトを調べられますが、`/workspace` 経由では変更できません。レポートは別の出力ディレクトリに書き込みます。

## Workload から見えるファイル

[Mount namespace](namespace.md) を使うと、process のグループごとに何が mount されているかの見え方を変えられます。Linux の [`mount(2)` のドキュメント](https://man7.org/linux/man-pages/man2/mount.2.html) は、mount の設定とその基盤となるファイルシステムを区別しています。読み取り専用の bind mount は、その mount 経由の書き込みを遮断しますが、別の mount 経由でも元のファイルが読み取り専用になるわけではありません。ファイルの内容を隠すこともありません。[Workload](workload.md) が参照する必要のあるファイルだけを mount してください。

[用語集に戻る](index.md)
