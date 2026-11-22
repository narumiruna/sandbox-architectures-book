# Namespace

Namespace は、process ID、mount されたファイルシステム、ネットワークインターフェースなどのシステムリソースについて、Linux の process のグループに固有の見え方を与えます。Process を別々の namespace に入れても、別々の [kernel](kernel.md) が割り当てられるわけではありません。

## 例

あるテスト用 sandbox は mount namespace を使い、host のホームディレクトリを見せずに、プロジェクトディレクトリを `/workspace` でテストランナーに見せます。別の [process ID namespace](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html) を使うことで、テストランナーにはジョブの process だけが見え、host 上の無関係な process は見えません。

## 見え方の分離は権限ルールではない

Linux には、リソースに応じて [異なる種類の namespace](https://man7.org/linux/man-pages/man7/namespaces.7.html) があります。何を mount するかを変えても、workload 独自のネットワークの見え方は得られません。書き込み可能な [mount](mount.md) で共有したファイルは、権限が許せば変更できます。

Namespace は process に何が見えるかを決めます。ファイルに何ができるかはパスベースのアクセス制御が決め、[seccomp](seccomp.md) は system call をフィルタリングし、[control group](control-group.md) はリソース使用量を計測または制限します。

[用語集に戻る](index.md)
