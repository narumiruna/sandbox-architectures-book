# Sandbox session

sandbox session は、[sandbox](sandbox.md) サービスが一つのまとまりとして追跡する、実行の一回分または利用期間です。サービスは、一つの session 内の複数の要求にわたって [workspace](workspace.md) と worker の状態を保持することがあります。

## 例

Lamp の session には、ソースを編集する要求とテストを実行する要求があります。session 中、テストランナーは編集による変更を参照できます。サービスは session を閉じる際に workspace を破棄しても、テストレポートを [artifact](artifact.md) として保持できます。

## 重要になる場面

複数の要求で session を再利用するときは、一時停止、再開、後片付けの後にどのファイルと状態が残るかを確認してください。session を閉じると、別のストレージにある出力を消さずに、コマンドを停止して worker を解放できます。

「[sandbox のライフサイクル](../practice/operations/sandbox-lifecycle.md)」を参照してください。
