# Tool のアクセス認可 {#tool-authorization}

スクリプトが [tool](../../glossary/tool.md) を使えても、すべての呼び出しが [authorized](../../glossary/authorization.md)（認可済み）とは限りません。[Lamp の実例](from-issue-to-patch.md)では、スクリプトは読み取り専用の issue tool を 1 つ呼び出せますが、[host](../../glossary/host.md) が要求を 1 件ずつ確認します。スクリプトが読めるのは Lamp の issue `LAMP-17` だけで、Lamp のほかの issue や Cedar の issue は読めません。

## スクリプトが呼び出せる tool は何ですか？ {#which-tools-can-the-script-call}

host は、検索用のスクリプトを [restricted interpreter](../../glossary/restricted-interpreter.md) で実行します。tool の [allowlist](../../glossary/allowlist.md) にあるのは、プロジェクトと issue ID を引数に取る操作 `get_issue` だけです。スクリプトはシェルを使えず、ファイルシステムに直接アクセスすることも、任意のネットワーク接続を行うこともできません。ビルドや公開を行う tool も渡されません。別の Linux worker が Lamp のプログラムをコンパイルしてテストしますが、その worker に issue tool は渡されません。

この一覧は、スクリプトがどの操作を要求できるかを制限します。許可された操作がどのプロジェクトを読めるかまでは決めません。読み取り専用の操作でも、権限のない呼び出し元にデータを見せてしまうことがあります。

## 1 回の呼び出しで何ができますか？ {#what-can-one-call-do}

`get_issue` を実装する [host function](../../glossary/host-function.md) は、インタープリターの外で動きます。host はこの関数に、今回の実行で承認済みのアクセス範囲、つまり Lamp の `LAMP-17` の読み取りを渡します。スクリプトの引数は対象を指定するもので、アクセス権を与えるものではありません。ハンドラーはレコードを検索する前に、要求された操作、プロジェクト、issue が許可されているかを確認します。ローカルのテストデータを読むときは、認可されたプロジェクトと issue ID の両方を使います。issue ID の接頭辞だけでは、その issue がプロジェクトに属していることの証明にはなりません。

- **許可する：** `get_issue(project="Lamp", issue="LAMP-17")` は、issue のタイトルと誤った合計値についての報告だけを返します。[credentials](../../glossary/credential.md) やほかのレコードは返しません。
- **拒否する：** `get_issue(project="Cedar", issue="CEDAR-9")` はプロジェクトの確認で拒否されます。Cedar のテストデータは読まず、その issue が存在するかどうかも明かしません。
- **検索範囲を広げない：** `get_issue(project="Lamp", issue="CEDAR-9")` は、今回の実行で許可された issue かどうかの確認で拒否されます。代わりに、プロジェクト全体の読み取りを許可する設定になっている場合でも、tool は Lamp 内だけを検索して該当なしと返します。全プロジェクトを対象に検索し直してはいけません。

返された issue のテキストはデータとして扱います。報告に別のプロジェクトを読むようスクリプトへ求める文があっても、host が渡した権限は変わりません。

## ハンドラーを単体で確認する {#check-the-handler-on-its-own}

両方のプロジェクトのダミーレコードと、Lamp の `LAMP-17` だけを許可するコンテキストを用意し、host のハンドラーを直接テストします。許可された呼び出しで意図したフィールドだけが返ることと、どちらのプロジェクトでもほかの issue が検索前に拒否されることを確認します。ここでテストするのは、インタープリターから切り離したこのハンドラーであり、ほかのインターフェースでのアクセス確認ではありません。[ローカルでのアクセス確認](../verification/verifying-access-rules.md)では、稼働中の issue トラッカーを使わず、より単純なプロジェクト単位のルールを実演します。

次は、[workspace と artifacts](../data-and-access/workspaces-and-artifacts.md)で、ソースのコピーが worker に入り、2 つのテキストファイルが出てくるまでをたどります。
