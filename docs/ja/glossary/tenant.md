# Tenant

tenant は、サービスが作業やデータを他と分けて扱うユーザー、チーム、または組織です。tenant は誰のリソースと権限が関係するかを示し、実行中のコードを分離する仕組みではありません。一つの tenant は複数の sandbox session を持てます。

## 例

二つのチームがビルドサービスを使います。一方はライブラリとドキュメントをビルドするために別々の [sandboxes](sandbox.md) を起動します。他方も自身の sandbox を起動します。最初の二つは同じ tenant に属しますが、三つ目からは、そのどちらのソースツリーもビルド結果も読めてはいけません。

## tenant ごとにリソースを分ける

[control plane](control-plane.md) はどの tenant が sandbox を起動または確保できるか、どの workspace を接続するかを確認します。複数の tenant に対応する [tool](tool.md) handler も、呼び出し元の tenant が要求したデータを使えるか確認する必要があります。サービスが提供する身元情報を使い、スクリプトが送った tenant 名を、その tenant のリソースを使う権限と見なさないでください。

tenant は必ずしも [isolation unit](isolation-unit.md) ではありません。サービスは一つの tenant でもジョブごとに別の VM を割り当てることがあります。保存した出力、キャッシュ、復元した [snapshots](snapshot.md) も対象の tenant の範囲内に保つ必要があります。VM を分けても、共有サービスが別の tenant のデータを返す問題は解決しません。

[用語集に戻る](../glossary.md)
