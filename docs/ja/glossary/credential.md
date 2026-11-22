# Credential

Credential とは、要求しているのは誰か、どのアクセス権を持つかを、サービスが確認するために使うものです。たとえば API トークンは、プログラムがアクセス権を得るためにサービスへ送れる値です。Sandbox 内のコードが再利用できる Credential を受け取ると、意図していた一つの操作以外にも使える場合があります。

## 例

Sandbox は Issue のタイトルを必要としています。Sandbox の外で実行される [tool](tool.md) は、その Issue が承認済みのプロジェクトに属することを確認します。ツールは読み取り専用トークンを Issue 管理システムに送り、Sandbox にタイトルを返します。トークンを扱うのはツールと Issue 管理システムで、Sandbox 内のコードはタイトルだけを受け取ります。

## Credential を使える主体

有効な [bearer token](https://www.rfc-editor.org/rfc/rfc6750.html#section-1.2) を手に入れた人は誰でも、サービスが受け付ける場所でそれを使えます。Sandbox 内のコードがファイルやプログラムの設定からトークンを読み取れるなら、それを直接使えます。コピーがログや、プログラムのメモリーを保存する [snapshot](snapshot.md) に残ることもあります。

[least privilege](least-privilege.md) を適用します。タスクに必要な操作とリソースだけへのアクセスを許可し、有効期間が短い Credential を優先します。コードに必要なのが Credential ではなく結果なら、Host 側のツールや [credential injection](credential-injection.md) を使い、プログラムに Credential を渡さずに済みます。

[用語集に戻る](index.md)
