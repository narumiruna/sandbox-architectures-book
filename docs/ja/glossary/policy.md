# Policy

Policy は、実行中のコードに許す操作と、使用を許すリソースを定めた一連のルールです。ルールが効力を持つのは、信頼できるコンポーネントが適用するときだけです。モデルに指示するだけではアクセス制限になりません。

## 例

Lamp のテスト用 [sandbox](sandbox.md) は、`total.c` を読み取って一時出力を書き込めますが、[host](host.md) の SSH 鍵は開けません。[Process sandbox](operating-system-process-sandbox.md) では、sandbox の設定でプロジェクトファイルを読み取り専用にし、一時ディレクトリを書き込み可能にします。Host の [kernel](kernel.md) は個々のファイルリクエストをこの設定と照合します。鍵はテストランナーからは見えません。

## 各ルールを適用するコンポーネントを決める

[Control plane](control-plane.md) は sandbox の作成時に policy を選べます。[Runtime](runtime.md)、オペレーティングシステム、proxy、[tool](tool.md) の handler は、それぞれが観測できる範囲のルールを適用します。たとえば [Linux kernel のドキュメント](https://docs.kernel.org/userspace-api/seccomp_filter.html) によると、[seccomp](seccomp.md) は kernel へのリクエストをフィルタリングできますが、リクエストがメモリー上のファイル名の位置しか渡さない場合は、フィルターでファイル名を読み取れません。ファイルへの直接アクセスについてパスのルールを適用するには、ファイルシステムの制御機能を使います。

## 注意が必要な場面

Sandbox を設定またはテストするときは、各 [isolation boundary](isolation-boundary.md) で何が成功し、何が失敗すべきかを確認します。同じリソースに [mount](mount.md) と tool の両方でアクセスできるなら、両方の経路を確認してください。一方の経路で拒否されても、もう一方で拒否されるとは限りません。ファイルアクセスのルールを構成する 2 つの部分については、[ファイルを開くリクエストを追う](../sandbox-isolation-boundaries.md#follow-a-request-to-open-a-file) を参照してください。

[用語集に戻る](index.md)
