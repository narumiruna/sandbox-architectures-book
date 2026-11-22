# Operating-system process sandbox

Operating-system process sandbox は、プログラムを [host kernel](kernel.md) 上で直接実行し、そのオペレーティングシステムの制御機能で、プログラムが何にアクセスできるか、どのような操作ができるかを制限します。別の [guest](guest.md) kernel は起動しません。

## 例

ローカルのコードレビュー用 sandbox は、プロジェクトの読み取り権限と一時出力ディレクトリへの書き込み権限を与えて、host の検索ツールを実行します。ツールに別のオペレーティングシステムは不要ですが、ツール本体とその子 process の両方に同じ制限を適用する必要があります。

## 組み合わせて使う制御機能

Linux では、[namespace](namespace.md) によって、mount 済みのファイルシステムやネットワークインターフェースの見え方を制限できます。[Linux 6.12 Landlock ガイド](https://docs.kernel.org/6.12/userspace-api/landlock.html#layers-of-file-path-access-rights) にあるようなパスベースのルールでは、ファイル階層に対する操作を制限できます。[Seccomp](seccomp.md) は system call をフィルタリングし、[cgroups](control-group.md) はリソース使用量を計測して制限します。これらの制御機能は互いに代用できません。Policy が何を許可し、sandbox が起動するプログラムだけでなく子 process にも適用されることを確認してください。

[用語集に戻る](../glossary.md)
