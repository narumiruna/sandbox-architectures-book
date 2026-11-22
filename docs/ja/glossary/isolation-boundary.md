# Isolation boundary

Isolation boundary は、実行中のコードをほかのコードやリソースから分離する仕組みです。直接アクセスを遮断しつつ、選んだリソースに制御された経路でアクセスさせることができます。境界は仕組みであり、何がそこを通過してよいかは [policy](policy.md) が定めます。仕組みの名前だけでは、コードが何にアクセスできるかは分かりません。

## 例

Lamp のテストジョブは、[sandbox](sandbox.md) を実行環境として使います。この環境は [virtual machine (VM)](virtual-machine.md) を利用して構成されています。サービスは、テストランナーに `total.c` のコピーを渡すことも、書き込み可能な共有領域でプロジェクトを公開することもできます。どちらにも VM の境界はありますが、テストジョブが元のファイルを直接変更できるのは、書き込み可能な共有領域を使う場合だけです。

## 仕組みが分離するもの

VM は guest のオペレーティングシステムを [host](host.md) から分離します。[Operating-system process sandbox](operating-system-process-sandbox.md) は、[process](process.md) の動作を制限しますが、その process は引き続き host の [kernel](kernel.md) を使います。一方、言語の [runtime](runtime.md) では、スクリプトが使える操作と [host function](host-function.md) を限定できます。詳しい比較は [Sandbox の isolation boundary](../sandbox-isolation-boundaries.md) を参照してください。

## 注意が必要な場面

信頼できないコードの実行環境を選ぶときは、保護すべきリソース、policy を適用するコンポーネント、そのコンポーネントが公開する経路を確認します。次に [isolation unit](isolation-unit.md) を特定します。同じ VM 内の 2 つのジョブはどちらも境界の内側にあるため、その VM の境界では互いに分離されません。

[用語集に戻る](../glossary.md)
