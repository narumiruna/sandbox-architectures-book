# Egress

Egress は、Sandbox の境界を越えて外へ出るネットワーク通信です。Egress の [policy](policy.md) は、Sandbox が接続できる外部サービスを制限できます。サービスへの接続を許可すること自体は、そのサービス上で Sandbox が何をできるかの制限にはなりません。

## 例

Sandbox がテストサーバー上のサンプルレコードを読み取るテストを実行します。ゲートウェイは読み取りを許可しますが、レコードの変更や他のサービスへの接続を求める要求は遮断します。要求は Sandbox から外に出て、応答は中に戻ります。

## 外向きの通信ルールを適用する場所

ファイアウォールは、ネットワークアドレスとポートの [allowlist](allowlist.md) を適用できます。読み取りと書き込みを区別する必要があるなら、Web プロキシなど、要求を読み取れるコンポーネントを使うか、サービス自体で操作を制限します。対象の経路上で信頼できるコンポーネントがルールを適用する必要があります。プロキシを設定するだけでは直接接続を制限できません。

ネットワークアクセスと、[tool](tool.md) 経由で公開する操作とは、別々に確認します。直接ネットワークにアクセスできなくても、Sandbox は代わりに要求を送る Host 側のツールを呼び出せる場合があります。そのツールでも独自に Authorization を確認する必要があります。

## 接続と応答

外向きの要求への応答は、Sandbox 内に入るため [ingress](ingress.md) の通信です。ネットワーク制御では、Sandbox が開始した接続への応答を許可しつつ、外部クライアントからの新規接続は許可しないようにできます。[Kubernetes 1.35 のネットワークポリシー](https://github.com/kubernetes/website/blob/03c191bcc446f9c15a9e68d6cd1154b53bde4291/content/en/docs/concepts/services-networking/network-policies.md#the-two-sorts-of-pod-isolation)は、クラスターのネットワークソフトウェアが適用すると、このように動作します。

[用語集に戻る](../glossary.md)
