# アクセスルールの検証 {#verifying-access-rules}

許可された操作が成功し、拒否された操作が**ルールによって**失敗することをテストします。たとえば、worker がファイルを読み取れない場合は、そのファイルを公開すれば同じ worker が読み取れることを先に確認します。そうしないと、入力ミスや起動の失敗を、意図どおりの拒否と見間違えることがあります。

## 結果を予測する {#predict-the-results}

この演習では、架空の [Lamp の issue 処理の流れ](../design/from-issue-to-patch.md)を使います。前の手順で使った virtual machine の代わりに、ローカルの [operating-system process sandbox](../../glossary/operating-system-process-sandbox.md) を使います。[Bubblewrap 0.11.1](https://github.com/containers/bubblewrap/blob/v0.11.1/README.md) が境界を設定し、Linux の [kernel](../../glossary/kernel.md) が [policy](../../glossary/policy.md) を強制します。C プログラムのビルドは、guest の kernel ではなく、host の kernel を使います。

[mount](../../glossary/mount.md) は、host 上のパスを worker 内で利用できるようにします。[namespace](../../glossary/namespace.md) は、process から見えるリソースの範囲を分けます。確認を実行する前に、ランナーがルールを 1 つずつ変えたとき、次のどの結果が変わるかを予測します。

| 確認すること | worker の policy で想定される結果 | ルールを 1 つ変えた場合との比較 |
| --- | --- | --- |
| 割り当てられた入力を読み取り、結果を書き込む | worker は割り当てられた Lamp の目印を読み取り、専用の一時領域で修正済みのコードをビルドしてテストし、`change.patch` と `test.log` を保存します。 | 許可されたこれらの操作には比較は不要です。 |
| 入力のコピーに書き込む | 同じ書き込みで `EROFS`（読み取り専用ファイルシステム）が返り、host 上にファイルは作られません。 | 同じ一時入力を読み書き可能な mount で公開すると、書き込みが成功します。 |
| 別の workspace の `/lab/other/marker` を読み取る | 読み取りで `ENOENT`（ファイルやディレクトリが存在しない）が返ります。Cedar は mount されていません。 | ダミーの Cedar workspace を mount すると、同じパスを読み取れます。 |
| host のループバック（`127.0.0.1`）にあるテストサービスからダミーの応答を読み取る | 接続で `ECONNREFUSED`（接続拒否）が返ります。worker のネットワーク namespace では、そのポートで待ち受けているサービスがありません。 | ネットワークを共有すると、同じアドレスとポートで `Lamp test service` が返ります。 |

1 回だけ応答する TCP サービスは、OS が選んだポートでループバックにだけバインドし、確認が終わると終了します。外部サービスや実データは使用しません。Linux の [network namespaces](https://man7.org/linux/man-pages/man7/network_namespaces.7.html) は、インターフェース、経路、ポート番号を分離します。この比較でテストするのは、host 上の指定された待ち受け先へのアクセスです。外向きの接続先リストや本番ネットワークをテストするものではありません。

## ローカルで確認を実行する {#run-the-local-checks}

x86-64 の Linux で root ではないアカウントを使います。次の前提条件を満たすよう、あらかじめ準備します。

- 非特権で user、mount、PID、IPC、UTS、network の各 namespace を使える Bubblewrap が必要です。この演習は `/usr/bin/bwrap` のバージョン 0.11.1 でテストしました。host や外側の container によっては、namespace の作成が禁止されていることがあります。
- `/bin`、`/lib`、`/lib64` が `/usr` 内を指す、`/usr` を統合したシステムが必要です。sandbox は `/usr/bin/python3`（Python 3.14.4 でテスト済み）と、システムのアセンブラ、リンカ、C 開発用ヘッダーを備えた `/usr/bin/gcc`（GCC 15.2.0 でテスト済み）を使います。
- host のスクリプトを実行するには [uv](https://docs.astral.sh/uv/getting-started/installation/) が必要です。以下のコマンドはインストール済みの Python を使い、プロジェクトのセットアップを省略し、パッケージを取得しません。

チェックアウトした本書のリポジトリのルートから、次を実行します。

```bash
uv run --offline --no-project --python /usr/bin/python3 python -B examples/lamp/lab.py verify
```

`PASS` が 8 行表示され、最後の行は次のとおりです。

```text
PASS: Lamp compiled and passed its test; change.patch and test.log verified
```

**`EROFS`**、**`ENOENT`**、**`ECONNREFUSED`** が出て、それぞれの比較で操作が成功していることを確認します。Bubblewrap のセットアップエラーは、操作が拒否された証拠ではなく、実験の失敗です。host が namespace を禁止しているか、必要なディレクトリ構成を備えていない場合は、互換性のある Linux テストシステムを使います。確認を通すために、隔離のオプションを外したり、host のセキュリティ設定を変えたり、root として実行したりしてはいけません。

[Ubuntu WSL2 テストシステム](measuring-a-sandbox.md#interpret-one-run)では、8 つの確認項目がすべて合格しました。ランナーは、入力の `total.c` が変わっていないこと、`change.patch` が引き算を足し算に置き換えていること、`test.log` に `PASS: total(2, 3) = 5` が含まれることを確認しました。その後、一時ファイルを破棄しました。[テスト用データとランナーのソース](https://github.com/narumiruna/sandbox-architectures-book/tree/main/examples/lamp)は `examples/lamp/` にあります。

## 証拠を読み解く {#interpret-the-evidence}

比較で操作が成功したことから、ファイルが存在し、許可されれば操作できると分かります。拒否を確認するテストでは、この設定で worker が Lamp の入力を読み取ることはできても書き込めず、指定した Cedar のパスも見えないと分かります。ただし、すべてのパス、process、ネットワーク経路をテストしたわけではありません。worker は mount された `/usr` を読み取れます。また、host の kernel を引き続き共有します。この演習では resource limits を設定せず、kernel への攻撃に対する耐性、継承されたシークレット、VM の隔離、本番環境での tenant の識別もテストしません。信頼できるテスト用データだけを使ってください。実際の運用では、使用する runtime、mount、identity のルール、許可するネットワーク接続先で、これらの確認をやり直します。[候補の評価チェックリスト](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)も参照してください。

## Tool の authorization を別に確認する {#check-tool-authorization-separately}

Linux の境界は、[host tool](../../glossary/host-function.md) を通じて誰が issue を読み取れるかを決めません。[authorization](../../glossary/authorization.md) のハンドラは別にテストします。以下の例では、模擬データと、[Tool の authorization](../design/tool-authorization.md)で説明する、Lamp プロジェクト全体を対象としたより単純な権限付与を使います。この例は Bubblewrap の外で実行し、issue トラッカーには一切接続しません。

```bash
uv run --offline --no-project --python /usr/bin/python3 python - <<'PY'
issues = {("Lamp", "LAMP-17"): "Incorrect item total", ("Cedar", "CEDAR-9"): "Dummy issue"}


def lookup_as_lamp_reviewer(project, issue):
    if project != "Lamp":
        raise PermissionError(project)
    return issues[project, issue]


if lookup_as_lamp_reviewer("Lamp", "LAMP-17") != "Incorrect item total":
    raise SystemExit("FAIL: expected the Lamp issue")
for project, issue, expected in (("Cedar", "CEDAR-9", PermissionError),
                                 ("Lamp", "CEDAR-9", KeyError)):
    try:
        lookup_as_lamp_reviewer(project, issue)
    except expected:
        continue
    raise SystemExit(f"FAIL: {project}/{issue} should fail with {expected.__name__}")
print("PASS: authorized lookup, project denial, and no cross-project fallback")
PY
```

次は [Sandbox の計測](measuring-a-sandbox.md)です。アクセスの確認は行わず、同じ C の workload にかかる時間を計測します。
