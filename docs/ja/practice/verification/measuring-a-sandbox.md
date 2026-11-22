# Sandbox の計測 {#measuring-a-sandbox}

呼び出し元が最初の出力を受け取る時点と、作業が完了する時点の**両方**を記録します。worker の応答が速くても、コンパイル、テスト、結果の書き込みが終わるまでには、はるかに長くかかることがあります。時間を比較する前に、[アクセスルールを検証します](verifying-access-rules.md)。必要なルールを強制できない worker は、速くても候補にはなりません。

## 毎回同じ workload を使う {#use-the-same-workload-each-time}

[workload](../../glossary/workload.md) とは、sandbox が実行するコードと process のことです。この演習では、アクセスの確認に使った [Lamp のタスク](../design/from-issue-to-patch.md)を使います。`total.c` のコピーで引き算のバグを修正し、GCC で C プログラムをビルドし、2 足す 3 が 5 になることを確認して、パッチとテストログを書き出します。毎回、同じテスト用データを同じ [Bubblewrap の process sandbox](../../isolation/native-programs/operating-system-process-sandboxes.md) で実行し、サービスの呼び出しや人為的な遅延は加えません。

| 計測項目 | 計測を止める時点 |
| --- | --- |
| 最初の出力までの時間 | 呼び出し元が `LAMP-17: loaded` を受け取った時点です。worker はテスト用データを読み取った後、修正済みのコードをコンパイルしたりテストしたりする前に、この行を出力します。 |
| 完了までの時間 | 呼び出し元が worker の出力をすべて読み取り、worker の終了を確認した時点です。成功した実行では、プログラムのビルドとテストが済み、`change.patch` と `test.log` の書き込みが完了しています。 |

どちらも host が Bubblewrap を起動する直前から計測するので、process sandbox の作成と Python の起動が含まれます。起動前の入出力ディレクトリの準備、終了後の artifact の確認と workspace の削除、リモートキューでの待機や artifact の転送は、どちらの計測にも**含めません**。実際の運用では、これらの段階も利用者の待ち時間に影響するなら計測します。

## 毎回新しい環境で 10 回起動する {#run-ten-fresh-launches}

[アクセスルールの検証](verifying-access-rules.md#run-the-local-checks)に記載された Linux、Bubblewrap、Python、GCC、`uv` の前提条件に従います。チェックアウトした本書のリポジトリのルートから、次を実行します。

```bash
uv run --offline --no-project --python /usr/bin/python3 python -B examples/lamp/lab.py measure
```

ミリ秒単位の 2 つの時間（`first_output_ms` と `completion_ms`）が 10 行表示され、その後に各計測項目の最小値、中央値、最大値が表示されます。ランナーは起動のたびに、終了ステータスが 0 であること、想定した出力が 2 行ともあること、想定したパッチとログがあることを確認します。実行に失敗した場合、その回の時間を報告するのではなく、演習を中止します。

起動するたびに、入力のコピー、出力ディレクトリ、sandbox を新しく作ります。永続的なビルドキャッシュはなく、host のファイルシステムキャッシュを消去したり、その状態を記録したりもしません。2 回目以降の起動では、コンパイラやライブラリを読み取った際のキャッシュを再利用することがあります。sandbox が新しくても、host のキャッシュが空とは限りません。別の候補と比較する場合は、host、kernel、tool のバージョン、runtime の policy、同時実行数、workspace とキャッシュをどのように準備または再利用したかを記録します。

## 計測結果の一例を読み解く {#interpret-one-run}

WSL2 上の Ubuntu 26.04.1 LTS（Linux 6.18.33.2、x86-64、AMD Ryzen 9 7950X3D、host の一時ファイルは `tmpfs` 上）で 10 回続けて実行したときは、Bubblewrap 0.11.1、Python 3.14.4、GCC 15.2.0 を使用しました。ランナーは毎回新しい workspace を作りました。この計測の前にアクセスを確認しました。host のキャッシュの消去も、状態の記録も行っていません。

| 計測項目 | 中央値 | 最小値～最大値 |
| --- | ---: | ---: |
| 最初の出力までの時間 | 24.37 ms | 21.49–26.48 ms |
| 完了までの時間 | 62.23 ms | 58.47–63.94 ms |

呼び出し元は、結果がそろうよりもかなり早く最初の行を受け取りました。最小値と最大値の差から、この小さなタスクでさえ、1 回の起動だけでは特性を把握できないことが分かります。これは計測方法の例であり、性能の基準値でも、製品の順位付けでもありません。

実際の候補を測るときは、workload を固定し、起動の計測に何が含まれるかを明示します。[cold start](../../glossary/cold-start.md)、[warm pool](../../glossary/warm-pool.md) からの割り当て、[snapshot](../../glossary/snapshot.md) からの復元では、行う処理が異なります。この例では、VM や warm pool、メモリ、ディスク使用量、負荷がかかった状態での起動、artifact の転送は計測しません。worker のピークメモリ使用量を計測するには、1 つの process のピーク [resident set size](../../glossary/resident-set-size.md) ではなく、専用の [control group](../../glossary/control-group.md) またはバックエンドの同等の集計機能を使用します。サービスが再利用できる状態については [Sandbox のライフサイクル](../operations/sandbox-lifecycle.md)を、ほかの比較項目については[候補の評価チェックリスト](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)を参照してください。

次は [Sandbox サービスの規模を拡大する](../operations/scaling-a-sandbox.md)です。キューでの待ち時間を比較し、テスト用の 2 つの tenant で切り替えの予行演習を行います。
