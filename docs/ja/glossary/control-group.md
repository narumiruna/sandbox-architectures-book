# Control group (cgroup)

Control group（cgroup）は、Linux の Process をまとめ、CPU 時間やメモリーなどのリソース使用量をオペレーティングシステムが測定または制限できるようにする仕組みです。Process がどのファイルを開けるか、どのネットワーク接続先に到達できるかを決めるものではありません。

## 例

ビルド用の Sandbox では、コンパイラーとその Worker Process を一つの cgroup にまとめます。サービスはジョブ全体のメモリー使用量を測定し、マシンのメモリーを使い切らないよう制限を設定できます。

## Linux がグループ単位でリソースを管理する方法

[Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) では、グループは木構造を形成します。*Controller* は、グループごとに特定のリソースを管理する [kernel](kernel.md) の構成要素です。たとえば、CPU Controller はグループの CPU 時間を制限でき、メモリー Controller はグループのメモリー使用量を追跡し、その上限を適用できます。

リソースの見え方を分けるには [namespace](namespace.md) を、ファイルやネットワークへのアクセスを制御するには別の [policy](policy.md) を使います。これらの制御は、リソース使用量の集計や制限とは役割が異なります。

[用語集に戻る](index.md)
