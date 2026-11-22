# ネットワークの policy {#network-policy}

[Lamp の手順解説](../design/from-issue-to-patch.md)に登場する worker は、自分の環境の外にあるネットワークのエンドポイントに接続しなくても、ビルドとテストを実行できます。issue tool は、[host](../../glossary/host.md) 上にあるサンプルのローカルレコードを読み取ります。[workspace サービスと artifact の収集コンポーネント](workspaces-and-artifacts.md)は、実行の前後に使い捨ての仮想ディスクを介して入力と出力を受け渡します。どちらにも worker のネットワークポートは不要です。

## 外向きの通信：必要な宛先だけを許可する {#outbound-allow-only-required-destinations}

[Egress](../../glossary/egress.md) は、worker の境界の外に出るネットワーク通信です。host は Lamp の [virtual machine (VM)](../../glossary/virtual-machine.md) に仮想ネットワークアダプターを割り当てません。worker は起動時にコンパイラ、ソース、テストを受け取るため、この設計では例外は不要です。worker のコードは、host のネットワークを使って issue ストア、依存パッケージのリポジトリ、他の worker、control plane にアクセスすることはできません。

将来のビルドで依存パッケージが必要になった場合は、worker に egress を許可するのではなく、別の取得サービスに承認済みパッケージの取得を許可します。以下の CI の例では、それらの権限を分ける方法を示します。ミラーに認証が必要な場合は、[Credentials と ID](credentials-and-identity.md)で説明するように、認証に使う情報は worker の外で管理します。

テストの別パターンでクライアントとサーバーを組み合わせて動かす必要がある場合は、その VM の内部からしかアクセスできないループバックのエンドポイントを利用できます。基準となる `LAMP-17` の実行では、そのようなサービスは使いません。

## 事例：パッケージを必要とする CI ジョブ {#case-a-ci-job-that-needs-packages}

[continuous integration (CI) job](../design/deployment-patterns.md#continuous-integration-ci) が、JavaScript 版の Lamp のテストを実行するとします。`LAMP-17` とは異なり、このジョブにはベースイメージに含まれていないパッケージが必要です。必要なのはパッケージのファイルであり、インターネットへの自由なアクセスではありません。テスト用 worker はオフラインのままにし、取得サービスだけに承認済みミラーへの egress を許可します。

1. **入力を承認します。** パッケージの取得元と完全性の検証値を記録した [npm v11.6.2 lockfile](https://github.com/npm/cli/blob/v11.6.2/docs/lib/content/configuring-npm/package-lock-json.md#packages) をレビューします。Lamp が直接指定したパッケージだけでなく、依存関係全体を解決します。未レビューのパッチによる lockfile の変更は、新たなパッケージを取得する許可とはみなしません。
2. **プロジェクトのコードを実行せずに取得します。** 取得サービスには、承認済みパッケージのコピーを配信する架空の依存パッケージミラー `deps.lamp.test` から、承認済みアーカイブだけを要求することを許可します。ミラーの [credential](../../glossary/credential.md) があれば、そのサービス内で管理します。許可していないメソッドやパッケージパス、および未承認の宛先へのリダイレクトは拒否します。アーカイブを配置する前に、承認済みの検証値と照合します。
3. **境界の内側でインストールとテストを行います。** あらかじめ用意したパッケージキャッシュのコピーを worker 専用に渡します。この事例では、インストールスクリプトが不要なパッケージを使います。キャッシュがすべてそろっていれば、[`npm ci`](https://github.com/npm/cli/blob/v11.6.2/docs/lib/content/commands/npm-ci.md#description) は [`--offline`](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js#L1353-L1361) と [`--ignore-scripts`](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js#L860-L872) を使って lockfile に基づくインストールを実行できます。worker の境界では、引き続きネットワーク通信を拒否します。これらのフラグで、テストやその子 process が実行できる操作を制御できるわけではありません。

キャッシュがそろっている場合と、欠けている場合の両方で、この設計案を確認します。承認済みアーカイブがすべてあれば、インストールとテストは成功するはずです。1 つでも欠けていれば、レジストリに接続せずにインストールが失敗するはずです。また、取得サービスが未承認のアーカイブを拒否すること、承認済みのアーカイブでもバイトが改変されていれば拒否すること、worker がミラーに直接接続できないことを確認します。これらは CI デプロイメントの受け入れ条件を確認するものであり、ローカル環境での Lamp の演習結果ではありません。

## 内向きの通信：プレビューが必要な場合にだけ許可する {#inbound-no-access-unless-someone-needs-a-preview}

[Ingress](../../glossary/ingress.md) は、境界の外から内に入るネットワーク通信です。仮想ネットワークアダプターがなければ、他の環境から worker に接続できません。`LAMP-17` の実行には、プレビュー URL も公開ポートもありません。レビュー担当者は別のレビュー用ストアにだけ接続し、そこでもアクセス権限が必要です。

将来の Lamp のタスクにブラウザーでのプレビューが必要になった場合は、呼び出し元の身元と、その Lamp session へのアクセス権限を確認するゲートウェイを介して、別のプレビューサービスを公開します。session が続いている間だけ、指定したプレビューサービスにのみ通信を転送します。テストのエンドポイントと他のすべての worker ポートには、引き続き外部からアクセスできないようにします。許可されたプレビュー接続への応答が認められていても、worker に新たな外向きの接続を開く権限が与えられるわけではありません。プレビューのリンクを知っているだけでは、アクセス権限は得られません。

[アクセスの確認手順](../verification/verifying-access-rules.md)を使って、想定どおりの通信と、policy が拒否すべき通信を区別します。確認に合格すれば、その経路についての証拠にはなりますが、すべてのネットワーク経路を網羅した証明にはなりません。

次の [Credentials と ID](credentials-and-identity.md) では、worker にサービスのシークレットを渡さずに、権限のある読み取りを許可する方法を説明します。
