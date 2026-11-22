# Workload

workload は、あるタスクのために環境が実行するコードと process です。sandbox では、単一のスクリプト、複数の process を使うビルド、agent session 全体などが該当します。workload は実行されるものであり、起動元のパッケージや起動するサービスではありません。

## 例

[agent](agent.md) は、どのテストを実行するか決めるために、生成されたスクリプトを一つの [sandbox](sandbox.md) で実行します。次に tool が、別の Linux sandbox でテストランナーと補助 process を起動します。スクリプトが一つ目の workload で、テストランナーと補助 process が二つ目を構成します。agent 自身はいずれの sandbox 内で動く必要もありません。

## 作業に合う境界の選択

必要な実行環境は workload によって異なります。複数の tool の結果をまとめるスクリプトなら、[restricted interpreter](restricted-interpreter.md) だけで足りる場合があります。特定のマシンと OS 向けにコンパイルされたプログラムである [native binaries](native-binary.md) を起動するビルドには、それらを実行できる互換環境が必要です。

[container image](container-image.md) は起動時のファイルと設定を提供するもので、実行中の workload ではありません。workload の child process が実際にどこで動き、どのリソースにアクセスでき、複数の workload が一つの [isolation unit](isolation-unit.md) を共有するかを確認してください。作業の種類に合った環境については「[Sandbox isolation boundaries](../sandbox-isolation-boundaries.md)」を参照してください。

[用語集に戻る](../glossary.md)
