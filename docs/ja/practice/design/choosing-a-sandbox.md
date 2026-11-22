# Sandbox の選び方 {#choosing-a-sandbox}

コードに何をさせる必要があり、何に触れさせてはいけないかを基準に、[sandbox](../../glossary/sandbox.md) を選びます。サービスの規模だけでは、どの程度強い境界が必要かは分かりません。個人のプロジェクトでも信頼できないコードを実行することがあります。一方、大規模なサービスでも、issue を読むだけのジョブがあります。

## 要件から判断の記録まで {#from-requirements-to-a-decision-record}

この手順は、[Lamp の判断記録のテンプレート](from-issue-to-patch.md#fill-in-your-decision-record)と併せて使います。

1. **できなければならないことと、アクセスできてはいけないものを挙げます。** [workload](../../glossary/workload.md) を誰が提供または変更できるかを記録します。対象には、ソース、テスト、ビルド手順、[agent](../../glossary/agent.md) が生成するコマンドが含まれます。必要なファイル、操作、接続を列挙します。ジョブが [host](../../glossary/host.md) の [kernel](../../glossary/kernel.md)（OS の中核部分）を使ってよいか、また、ほかのジョブと kernel を共有してよいかを決めます。
2. **製品を選ぶ前に [isolation boundary](../../glossary/isolation-boundary.md) を選びます。** [restricted interpreter](../../glossary/restricted-interpreter.md) を使えば、スクリプトが 1 つの読み取り専用 [tool](../../glossary/tool.md) にアクセスできるようにできます。それでも、tool は要求のたびに [authorization](../../glossary/authorization.md) を確認します。worker がコンパイラーや子プロセスを実行する必要があり、host の kernel を使ってはならない場合、[operating-system process sandbox](../../glossary/operating-system-process-sandbox.md) は要件を満たしません。worker に専用の Linux kernel が必要なら、[virtual machine (VM)](../../glossary/virtual-machine.md) を評価します。[実行場所と運用者](deployment-patterns.md)は別に決めます。
3. **どのジョブが 1 つの環境を共有するかを決めます。これが [isolation unit](../../glossary/isolation-unit.md) です。** たとえば、ジョブごとに新しい VM を用意する方式と、1 社の顧客が VM を再利用する方式では、境界の種類は同じですが、共有のルールは異なります。何を残せるか、何を削除する必要があるか、成功・失敗・キャンセルの後に誰が後片付けを確認するかを記録します。
4. **費用や速度を比べる前に、要件を満たすかをテストします。** 同じソースのリビジョン、テスト、ツールチェーンを使います。許可した操作が成功し、禁止した操作が意図した理由で失敗することを確認します。要件を満たした候補だけを比較します。キューでの待ち時間と準備時間を含め、ジョブの投入からレビュー可能な出力が得られるまでの時間を測ります。CPU、メモリ、ディスクの使用量とキャッシュの状態を記録します。ジョブあたりの運用費用がある場合は、その費用も記録します。テストの前に目標を設定します。各要件について、**文書で確認済み**、**測定済み**、**不明**のどれに当たるかを記録します。不明な要件は合格とみなしません。[候補の評価](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)と [sandbox の測定](../verification/measuring-a-sandbox.md)を参照してください。

## 同じ Lamp タスクに対する 3 つの判断 {#three-decisions-for-the-same-lamp-task}

3 つの環境すべてで、[Lamp のタスク](from-issue-to-patch.md)は `LAMP-17` を読み、小さな C プログラムの誤った合計値を修正し、修正版をコンパイルして、2 個と 3 個を足すと 5 個になることをテストします。検索用のスクリプトは restricted interpreter 内で、読み取り専用の issue tool だけを使います。別の Linux worker が、既知のリビジョンに固定した使い捨ての [workspace](../../glossary/workspace.md) を編集します。worker にネットワークアクセス、issue tool、リポジトリの [credentials](../../glossary/credential.md) は必要ありません。レビュー用の [artifacts](../../glossary/artifact.md) は `change.patch` と `test.log` だけです。認可されたレビュアーだけが読め、7 日後に失効します。worker は公開できません。以下の記録は設計案であり、テスト結果ではありません。

### Linux ワークステーション上の個人プロジェクト {#personal-project-on-a-linux-workstation}

- **要件：** 開発者が実行を開始しますが、agent のコマンドは信頼しません。worker とその子プロセスは、開発者のホームディレクトリや credentials の読み取りも、元のチェックアウトの変更もできないようにします。このプロジェクトでは、ワークステーションの kernel を共有してもかまいません。
- **境界と共有単位：** ネイティブツールは operating-system process sandbox で実行します。ビルドとテストは、今回の実行に限り 1 つの sandbox を共有します。
- **残すものと削除するもの：** インストール済みの読み取り専用ツールチェーンは再利用しますが、worker や以前のビルドディレクトリは再利用しません。プロセスツリーを停止し、作業用コピーとビルドファイルを削除します。2 つの出力は、保存期限まで、開発者のアクセス制限付きレビュー用ディレクトリに保持します。
- **この構成を選ぶ理由：** 通常のシェルには、このようなファイルアクセス制限がありません。別の guest kernel を設けると、このプロジェクトには不要な準備が増えます。
- **見直す条件：** 外部の協力者がビルドやテストを提供できるようになった場合、またはワークステーションの kernel を worker と共有できなくなった場合です。

### 社内の複数チーム向けサービス {#internal-service-for-several-company-teams}

- **要件：** チームのメンバーはビルドやテストを変更できます。worker は、host や別のジョブと kernel を共有してはいけません。issue の読み取り、workspace の接続、artifact の読み取りの前に、呼び出し元のチームとプロジェクトを確認します。誰がジョブを開始したか、対象のプロジェクトとリビジョン、実行結果を記録します。失敗した実行への対応と後片付けはプラットフォームチームが担当します。
- **境界と共有単位：** 社内の runner で、実行ごとに新しい Linux VM を起動します。同じチームの実行が連続しても、guest は共有しません。
- **残すものと削除するもの：** コンパイラーを含み、チームのデータを含まない読み取り専用のベースイメージを再利用します。guest を破棄し、作業用ストレージとビルドファイルを削除します。監査記録とチーム内に限定した 2 つの出力は、それぞれに適用される別々の保持ルールに従って保存します。
- **この構成を選ぶ理由：** host の kernel を使う process sandbox は、kernel を分けるというルールを満たしません。チームで VM を再利用するなら、実行の合間にリセットされることを確認する必要があります。失敗したジョブのファイルが再試行時に残らないよう、まずは再利用しない構成から始めます。
- **見直す条件：** 社内 API が必要になった場合、従業員以外が提供するコードを受け付け始める場合、またはキューの目標を達成できない場合です。アクセス制御が不足しているのか、単に worker が足りないのかを確認します。

### 互いに無関係な顧客向けの大規模サービス {#large-service-for-unrelated-customers}

- **要件：** 登録済みの顧客は誰でもコードを提供できます。[tenant](../../glossary/tenant.md) は、ほかの顧客からデータと処理を分離しておく必要がある顧客です。どのジョブも host や別のジョブと kernel を共有しません。issue の検索、workspace の接続、artifact の取得のそれぞれで、tenant ごとのアクセス制御を個別に適用します。[resource limits](../../glossary/resource-limit.md) と tenant ごとの同時実行数の上限を適用します。上限を超えるジョブは待機するか拒否されますが、処理容量に空きがあれば、別の tenant はジョブを開始できます。
- **境界と共有単位：** ジョブごとに新しい Linux VM を起動し、1 つの tenant に割り当てます。runner のハードウェアは policy が許す場合だけ共有し、顧客のジョブ間で guest を共有することはありません。
- **残すものと削除するもの：** 顧客データを含まない読み取り専用のベースイメージを再利用します。稼働中の guest や顧客のキャッシュは再利用しません。キャンセル時も guest と作業用ストレージを破棄します。パッチとテスト出力は、保存期限まで tenant 内に限定したレビュー用ストレージに保持します。再試行には新しいストレージを割り当てます。
- **この構成を選ぶ理由：** host の kernel を使う process sandbox も、共有 guest も、kernel のルールを満たしません。tenant ごとに VM を 1 台用意すれば、guest の境界で tenant を分離できますが、同じ tenant のジョブ同士は互いの状態に影響を与えることができます。VM を分けても、issue tool やストレージサービスの設定ミスは解消されません。
- **見直す条件：** 負荷がピークのときに、キューでの待ち時間、完了率、ジョブあたりの費用のいずれかが目標を満たさない場合です。runner の実行枠がボトルネックなら、処理容量を増やします。host の共有に関する前提が変わったら、境界または配置を見直します。再利用を有効にする前には、後から実行するジョブに何が見えるかを確認します。

[無害なアクセス確認](../verification/verifying-access-rules.md)で意図した経路と拒否すべき経路をテストし、共有サービスには [tenant の隔離の確認](../data-and-access/multi-tenant-isolation.md)を使います。ローカルでの確認だけでは、VM やサービスがそれらのルールを強制していることまでは確認できません。

## 公開されている 2 つのワークフローと異なる要件 {#two-public-flows-different-requirements}

[CodeRabbit Pull Request Reviews](https://docs.coderabbit.ai/overview/pull-request-review) は、プルリクエスト（PR）ですでに変更が提案された状態から始まります。[GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github) は、開発タスクから始めて新しい PR を提案できます。両者は異なる仕事をするもので、ベンチマークでも、Lamp の 2 つの実装でもありません。比較対象はこれらのワークフローだけで、CodeRabbit Coding Agent、Copilot code review、その他のモードは対象外です。比較は 2026 年 11 月 22 日に確認した公式文書に基づいており、製品をテストした結果ではありません。

| 確認項目 | CodeRabbit：既存の PR をレビューする | GitHub Copilot cloud agent：タスクを実装して PR を提案する |
| --- | --- | --- |
| 入力と出力 | PR を開くか、新しいコミットをプッシュすると、自動レビューが始まることがあります。CodeRabbit は変更と関連するリポジトリのコンテキストを使い、リンクされた issue があればそれも参照して、指摘と提案を既存の PR に投稿します。 | Agents タブでリポジトリを選び、Copilot にタスクの実装と PR の作成を依頼します。[issue を割り当てる](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github#assigning-an-issue-to-copilot)方法もあります。この場合、Copilot は issue のタイトル、説明、既存のコメント、追加の指示があればその指示も受け取ります。Copilot が新しい PR 用の変更を行い、人がレビューします。 |
| tool と権限 | リンターなどの[分析ツール](https://docs.coderabbit.ai/tools/index)が指摘事項を提供します。たとえば、[ESLint との連携](https://docs.coderabbit.ai/tools/eslint)では承認済みのプラグインだけが許可されます。レビューには新しいブランチは不要ですが、[GitHub App のインストール](https://docs.coderabbit.ai/platforms/github-com#review-permissions)では、コード、PR、チェックへの読み書き権限が要求されます。アプリの権限からは、個々の分析ツールにどの権限が与えられるかは分かりません。 | Copilot はリポジトリのコピーでコマンドやテストを実行できます。新しい PR を作る場合、[GitHub の文書](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations#copilot-cloud-agent-can-push-code-changes-to-your-repository)によると、呼び出し元にはリポジトリへの書き込み権限が必要です。Copilot がプッシュできるのは割り当てられたブランチだけで、PR の承認やマージはできません。 |
| 環境と隔離 | CodeRabbit の文書では、分析のためにリポジトリ全体をクローンする[クラウド上の sandbox](https://docs.coderabbit.ai/overview/architecture)について説明しています。その図には、複数の実行環境を持つ [Cloud Run](https://docs.cloud.google.com/run/docs/about-execution-environments) が記載されています。確認した資料からは、どの境界が適用されるか、どの実行や顧客が稼働中の環境や物理 host を共有できるかは分かりません。 | **Cloud** オプションについて、GitHub は、ユーザーのマシンやほかのセッションから隔離され、ネットワーク制限を設定できる[セッションごとの Linux sandbox](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/about-cloud-sandboxes)を説明しています。その説明だけでは、境界にどの技術が使われているか、誰が物理 host を共有できるかは分かりません。 |
| 残るもの | CodeRabbit の文書によると、ソースと依存関係を保持する再利用可能な [cache](https://docs.coderabbit.ai/reference/caching) がデフォルトで有効になっており、7 日以内に失効します。[FAQ](https://docs.coderabbit.ai/faq#data-security) では、これとは別に、より長く保持されるレビューのコンテキストを説明しています。cache の有効期限からは、すべてのレビューデータの削除期限は分かりません。 | [セッションデータ](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/session-data)の文書では、停止した Cloud セッションの [snapshot](../../glossary/snapshot.md) を保存し、ファイルや作業途中の状態を引き継いで再開できるようにすることを説明しています。確認した資料からは、すべてのコピーがいつ削除されるかは分かりません。PR とコミットは worker の状態とは別に残ります。 |

**どの環境に当てはまるかに注意してください。** GitHub は **Actions** 環境についても説明しています。GitHub がホストする Actions セッションでは、終了時にセッション環境は破棄されますが、ログは残ります。この後片付けのルールや Actions runner の特性が、デフォルトの **Cloud** オプションにも当てはまるとは考えないでください。

プロバイダーが運用するサービスを評価するときは、選んだモード、プラン、設定の文書を確認します。何が境界を越えられ、何が実行後に残り得るかを記録します。必要な特性が文書に記載されていない場合は、プロバイダーに根拠を求め、ダミーデータで確認可能なことを確かめます。「sandbox」という言葉だけを根拠に、VM を使っている、ジョブごとに新しい環境を用意する、すべてのデータを削除すると判断してはいけません。

次は、[デプロイのパターン](deployment-patterns.md)で、隔離方式の選択と、配置、運用責任、後片付けに関する判断を分けて考えます。
