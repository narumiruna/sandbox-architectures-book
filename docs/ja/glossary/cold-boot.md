# Cold boot

Cold boot とは、保存した実行状態を再開する代わりに、内部のオペレーティングシステムを起動して新しい [virtual machine](virtual-machine.md) を立ち上げることです。準備済みのディスクイメージを利用できるため、オペレーティングシステムをゼロからインストールする必要はありません。

## 例

ビルドサービスは、コンパイラーを含むディスクイメージから Linux の Sandbox を立ち上げます。VM 内で Linux が起動し、VM 内のサービスがビルドコマンドの受け付けを始めます。コンパイラーの Process やその他の実行中のプログラムは、以前の VM から引き継がれていません。

## 起動してから Sandbox が使えるまで

[virtual machine monitor](virtual-machine-monitor.md) が仮想ハードウェアを準備します。[guest kernel](guest.md) が起動し、その後 Guest がプログラムやサービスを立ち上げます。[リビジョン `42f413d` の NVX ライブラリーガイド](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/library.md#cold-boot)では Cold boot を例示し、別の経路として[保存したメモリーと VM の状態からの復元](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/library.md#restore-from-a-snapshot)を説明しています。

起動時間と利用可能になるまでの時間は分けて測定します。Guest の起動が完了しても、Sandbox にプロジェクトの Workspace がまだ接続されていなかったり、最初のコマンドをまだ実行できなかったりすることがあります。[cold start](cold-start.md) には Cold boot が含まれる場合もありますが、[snapshot](snapshot.md) を使って Guest の起動を省略することもできます。

[用語集に戻る](../glossary.md)
