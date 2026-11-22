# デプロイのパターン {#deployment-patterns}

worker をどこで動かし、誰が運用するかは、[sandbox が何を隔離するか](choosing-a-sandbox.md)とは別に決めます。リモートのインフラで動く worker は、自組織で運用することも、プロバイダーに運用を任せることもできます。4 つの構成すべてで、同じ読み取り専用の [tool](../../glossary/tool.md) が Lamp の issue `LAMP-17` を取得し、別の Linux worker が小さな C プログラムの誤った合計値を修正します。worker はコピーをコンパイルしてテストし、レビュー用にテキスト形式のパッチとテスト出力を返します。公開はできません。

## どの構成でも変わらないこと {#what-stays-the-same}

Linux worker には使い捨ての [workspace](../../glossary/workspace.md) を渡します。元のリポジトリを書き込み可能な [mount](../../glossary/mount.md) として渡すことはありません。issue tool は架空のテストデータを読み取り、サービスの [credentials](../../glossary/credential.md) は使いません。issue の読み取りに credentials が必要な場合、以下に示す管理者が、スクリプトと worker の両方の外で保管します。公開権限は、このワークフローの外にある別の役割に割り当てます。パッチとログは [artifacts](../../glossary/artifact.md) として保存し、アクセスをレビュアーに限定し、保存期限を明示します。

## 各構成を運用するのは誰ですか？ {#who-operates-each-layout}

### ローカルのワークステーション {#local-workstation}

開発者がスクリプトと Linux の両方の実行環境を運用し、issue tool と、読み取り用の credentials がある場合はそれも管理します。ローカルのコントローラーは作業用コピーを作成し、実行後は worker を停止してコピーを削除します。開発者はレビュー用ディレクトリへのアクセスを制限し、レビュー期間が終わると保存した出力を削除します。この構成ではワークフロー全体が開発者のマシン上で動きますが、それでも実行環境は、worker が開発者のホームディレクトリや元のチェックアウトにアクセスできないようにする必要があります。

### 継続的インテグレーション（CI） {#continuous-integration-ci}

[Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration)（CI、継続的インテグレーション）を使うと処理を自動で開始できますが、CI は隔離の仕組みではありません。この構成では、runner の運用者が 2 つの [runtimes](../../glossary/runtime.md) を保守します。プロジェクトチームはソースのリビジョンを選び、issue tool と、読み取り用の credentials がある場合はそれも管理します。また、artifacts を誰がいつまで読めるかを決めます。CI のジョブコントローラーは作業用コピーを準備し、失敗した場合も含めて処理後に削除します。CI の artifact ストレージでは、プロジェクトが定めた期限で保存済みの出力が失効します。ジョブは、リリース権限を引き継がずに、プロジェクトの既存のレビューワークフローを利用できます。

### 自組織で運用するサービス {#self-hosted-service}

社内のプラットフォームチームが両方の runtime を運用し、自ら運用するインフラ上で実行ごとに作業用ストレージを提供します。インフラの場所は自社施設でもクラウドでもかまいません。各プロジェクトチームは、自分たちのソース、issue tool とその読み取り権限、レビューへのアクセスを定める [policy](../../glossary/policy.md) を管理します。プラットフォームチームの [control plane](../../glossary/control-plane.md) は、失敗した worker や実行期限を過ぎた worker を停止し、作業用ストレージを削除し、保存した出力をプロジェクトの policy に従って失効させます。プラットフォームチームは runtime への修正パッチの適用、処理容量の監視、障害への対応も行う必要があります。

### プロバイダーが運用する worker サービス {#managed-worker-service}

顧客がスクリプトの runtime を運用し、issue tool と、読み取り用の credentials がある場合はそれも管理します。プロバイダーは Linux の runtime を運用し、worker の作業用ストレージを作成、削除します。顧客は使用するソースのコピーを選び、自分たちのレビュー用ストレージでアクセスと保存期限を管理します。キャンセル後も含め、プロバイダーが何を削除し、何を保持するかも顧客が確認する必要があります。ジョブが終わっても、ログ、キャッシュ、[snapshots](../../glossary/snapshot.md) などの別のコピーが削除されるとは限りません。

## 3 つのことを別々に決める {#make-three-separate-decisions}

1. **配置：** 承認済みのファイルをワークステーションや組織の外に出してもよいでしょうか。ジョブを実行する場所と、その状態や出力を保存する場所を記録します。
2. **運用責任：** runtime に修正パッチを適用し、失敗したジョブに対応し、後片付けを確認し、処理容量の費用を負担するのは誰でしょうか。自組織で運用する場合にかかる担当者の作業時間とインフラの費用を、プロバイダーが運用する場合の利用料金と顧客に残る作業と比較します。
3. **実行境界：** ローカルの worker でも [virtual machine (VM)](../../glossary/virtual-machine.md) を使えます。リモートの worker でも [host](../../glossary/host.md) の [kernel](../../glossary/kernel.md) を共有することがあります。どの runtime が [isolation boundary](../../glossary/isolation-boundary.md) を強制し、どのジョブがその境界を共有し、何がその境界を越えられるかを確認します。実装例については、[アーキテクチャの調査](../../agent-sandbox-architectures.md)を参照してください。

次は、[tool のアクセス認可](tool-authorization.md)でアクセスルールの設定を始めます。スクリプトが sandbox 内で動く場合でも、issue を検索する tool が何を確認すべきかを説明します。
