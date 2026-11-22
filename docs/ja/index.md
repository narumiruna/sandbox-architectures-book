# Sandbox Architectures Book

[sandbox](glossary/sandbox.md) は、プログラムがアクセスできる範囲を制限しながら、プログラムを実行する環境です。本書では、sandbox がその制限をどう強制するかと、実行するコードに合った境界をどう選ぶかを説明します。

数個の API を呼び出すだけの AI agent と、パッケージをインストールしてソフトウェアをビルドし、テストを実行する agent では、必要な環境が異なります。製品名からではなく、agent に任せる作業から考えましょう。

## ここから始める {#start-here}

まず **基礎** を読み、架空のコーディング課題 Lamp が、最初の実行から複数の顧客向けサービスになるまでを追います。隔離の仕組みをすでに知っている場合は、**sandbox を設計する** の実践例から始めてください。

1. **基礎。** [Sandbox の隔離境界](sandbox-isolation-boundaries.md) で、何がアクセス制限を強制するかを説明します。OS 上の workload や、言語またはモジュール用の runtime でコードを実行する 6 つの方式を見ていきます。
2. **Sandbox を設計する。** [課題からパッチまで](practice/design/from-issue-to-patch.md) では、課題の検索から人によるレビューまで、Lamp のデータと権限の流れを追います。次に、[sandbox を選び](practice/design/choosing-a-sandbox.md)、[どこで実行し、誰が運用するか](practice/design/deployment-patterns.md)を決めます。
3. **アクセスルールを設定する。** [Tool の authorization](practice/design/tool-authorization.md) から始め、作業の各部分で利用できるファイル、ネットワークの接続先、credential を決めます。異なる顧客やチームの作業とデータは分けてください。
4. **Sandbox を運用する。** まず [control plane](practice/operations/control-planes.md) の章で、何が worker を起動し、後片付けをするかを確認します。次に、worker の稼働期間の管理、リソース使用量の制限、障害の診断を学びます。
5. **Sandbox を検証する。** [アクセスルールが機能するかを確認し](practice/verification/verifying-access-rules.md)、[作業の実行を計測](practice/verification/measuring-a-sandbox.md)します。ローカル演習で示すのは検証方法であり、本番環境の安全性や速度を証明するものではありません。
6. **Sandbox サービスを拡張する。** 2 つのテスト用顧客を使って [Lamp の移行を予行演習](practice/operations/scaling-a-sandbox.md) します。worker を増やす必要があるのか、隔離方式を変える必要があるのか、あるいは両方が必要なのかを確認します。

## 参考資料を使う {#use-the-reference}

- [Agent 向け sandbox のアーキテクチャ](agent-sandbox-architectures.md) では、実際の実装を比較します。workload に必要な境界がわかったら、候補を探すために使ってください。
- [用語集](glossary/index.md) では、なじみのない用語の定義を調べ、詳しい解説に進めます。

## 本書を通して考える問い {#questions-to-carry-through-the-book}

1. **何を隔離する必要があるか？** Tool を使うスクリプト、process、それとも Linux workspace 全体でしょうか？
2. **何が境界を越えられるか？** Workload は、どのファイル、ネットワークの接続先、credential、tool にアクセスできますか？
3. **実行後に何が残るか？** Workspace、snapshot、キャッシュには、どのデータが残りますか？
