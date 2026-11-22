# Tool

tool は、issue の検索やビルドの開始など、agent やスクリプトが要求できる操作です。呼び出し元が入力を渡し、handler と呼ばれるコンポーネントが操作を実行します。tool を呼び出せることは、すべての要求を許可すべきだという意味ではありません。

## 例

リリース用スクリプトは [sandbox](sandbox.md) 内で動き、issue のタイトルを取得する tool を呼び出します。スクリプトは issue 番号を渡します。handler は、その issue がスクリプトに読み取りが許可されたプロジェクトに属することを確認し、タイトルだけを返します。handler は自身の [credential](credential.md) をスクリプトに渡さずに issue サービスを使えます。

## インターフェースと handler

tool のインターフェースは呼び出し元が何を要求できるかを示します。言語 sandbox では [host function](host-function.md) がスクリプトから handler への経路を提供できます。handler は [policy](policy.md) を適用します。呼び出し元が対象リソースに操作を実行できるか確認し、影響と結果を許可範囲に限定します。issue 番号の形式が正しくても、呼び出し元がその issue を読める証明にはなりません。

sandbox はスクリプトが呼び出せる tool を制限できますが、外部で動く handler にスクリプトと同じ制限は課せません。ビルド用 tool は、その [workload](workload.md) に適した別の sandbox でジョブを開始できます。この場合、スクリプトとビルドの境界はシステムの異なる部分を保護します。

[用語集に戻る](index.md)
