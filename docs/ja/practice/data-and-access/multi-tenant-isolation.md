# 複数 tenant の隔離 {#multi-tenant-isolation}

実行中のジョブを分離し、ジョブの終了後も残るデータへのアクセスを確認します。[Lamp の手順解説](../design/from-issue-to-patch.md)では、Lamp と Cedar は 2 つの [tenants](../../glossary/tenant.md)、つまり作業とデータを互いに分離する必要があるグループです。Cedar が ID やファイル名を知っていても、Lamp の issue、workspace、レビュー用の出力は読み取れないようにします。

## 何が境界を共有するか決める {#decide-what-shares-a-boundary}

[isolation unit](../../glossary/isolation-unit.md) は、1 つの [isolation boundary](../../glossary/isolation-boundary.md) のインスタンスを共有する [workloads](../../glossary/workload.md) の集まりです。何が 1 つのインスタンスを共有するかを決めることと、境界の仕組みを選ぶことは別です。[アーキテクチャの比較](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)では、同じく [virtual machines (VMs)](../../glossary/virtual-machine.md) を使っていても、作業をまとめる単位が異なるシステムを比較します。

| 境界を 1 つ割り当てる単位 | 利点 | 引き継がれる可能性があるもの |
| --- | --- | --- |
| リクエスト | ジョブごとにまっさらな状態から開始できます。 | 境界のインスタンスを置き換えれば、その内側に前のジョブの状態は残りません。外部ストアは引き続き確認が必要です。ジョブごとにセットアップを繰り返します。 |
| Session | 複数のステップで、エディター、workspace、ビルド出力を再利用できます。 | 同じ session 内では、リクエストをまたいでファイルや process が残ります。その session へのアクセスを許可された呼び出し元だけが再接続できます。 |
| Tenant | 同じ tenant のジョブが、長期間存続する 1 つの環境を使えます。 | 境界を追加しなければ、その tenant のジョブやユーザーは runtime を共有します。ジョブ間でその状態を共有してよい場合に限り適しています。 |

## 共有するリソースを明確にする {#keep-shared-resources-deliberate}

Lamp は、同じ tenant が再試行する場合でも、ビルドの試行ごとに新しい VM を 1 台起動します。[control plane](../../glossary/control-plane.md) は、確認済みの依頼者の身元をもとに、tenant と実行を VM に関連付けます。workspace サービスは、その関連付けを確認してから、その実行用の使い捨て [workspace](../../glossary/workspace.md) を `/work` に接続します。`lamp/work` のような名前はラベルであり、権限を確認する仕組みではありません。

ジョブ間では、クリーンな読み取り専用コンパイライメージを共有できます。workspace のディスク、実行中の VM、書き込み可能なキャッシュ（後で使う入力やビルド結果を保存する場所）は共有しません。この例では、ジョブのデータを接続した後に snapshot を保存しません。将来の設計で非公開キャッシュが必要になる場合は、そのサービスが項目を返す前に tenant のアクセス権限を確認する必要があります。

issue ハンドラーは呼び出しごとに tenant、操作、レコードを確認します。レビュー用ストアは読み取りごとに tenant と、その実行のレビュー担当者として指定されているかを確認します。Lamp に所属しているだけでは不十分です。その実行を担当するオペレーターが参照する診断記録も、tenant ごとに範囲を限定します。VM を分けても、これらのストアのいずれかが別の tenant にデータを渡す事態は防げません。

## ダミーデータで確認する {#check-with-dummy-data}

Lamp と Cedar のそれぞれに、ファイル名は同じで目印となるテキストだけが異なるダミーの workspace と artifact を用意します。各 tenant が自分の目印を読み取れる一方で、相手の workspace を接続したり、相手の artifact を取得したりできないことを確認します。許可された Lamp の呼び出し元だけが `LAMP-17` を読み取れることも確認します。非公開キャッシュがある場合は、tenant ごとに同じ項目名で異なる目印を置き、それぞれが自分の値を取得することを確認します。Lamp のジョブを実行した基盤で新しい Cedar のジョブを開始し、Lamp の目印が残っていないことを確認します。ローカル環境での例は [アクセスルールの検証](../verification/verifying-access-rules.md)を参照してください。これらの確認は、host を共有することによる影響をすべて網羅するものではありません。

次の [Control plane の役割](../operations/control-planes.md) では、サービスが worker を起動し、正しい tenant の workspace を接続して、クリーンアップを確認する流れを説明します。
