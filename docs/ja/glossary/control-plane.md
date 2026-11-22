# Control plane

Control plane は、実行環境を管理するシステムの一部です。たとえば、[sandbox](sandbox.md) をどこで実行し、いつ起動または停止するかを決めます。コードの動作を制限する仕組みを選んで設定できますが、それ自体が制限を行う仕組みではありません。

## 例

ビルドサービスが Lamp のテスト要求を受け取ります。Control plane は承認済みの設定から [virtual machine (VM)](virtual-machine.md) を起動し、Lamp の [workspace](workspace.md) を渡し、実行が終わったら VM を削除します。テストの実行中、`total.c` を開く要求を処理するのは Control plane ではなく、VM の [guest kernel](guest.md) です。

## 管理と実行の違い

Control plane は、実行用の [runtime](runtime.md) を選び、特定の Workspace を要求し、環境が利用可能かどうかを追跡できます。たとえば、[Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/README.md) は Kubernetes 上に管理 API を提供し、Sandbox の定義と確保を可能にします。[isolation boundary](isolation-boundary.md) は Runtime が提供するため、同じ種類の管理要求でも同じ種類の隔離になるとは限りません。

## 管理が重要な場面

多数のジョブが Sandbox を必要とするときは、Control plane を使って環境を割り当て、ジョブの終了後に片付けます。サービスは [authorization](authorization.md) によって、誰が環境を作成または確保できるか、誰のファイルを接続するかを判断しなければなりません。Control plane が別の [tenant](tenant.md) の Workspace を Sandbox に割り当てても、実行境界ではその誤りを直せません。[パッケージ化、管理、隔離を分ける](../sandbox-isolation-boundaries.md#keep-packaging-management-and-isolation-separate)を参照してください。

[用語集に戻る](../glossary.md)
