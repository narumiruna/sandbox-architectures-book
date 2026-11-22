# Process

process は、実行中のプログラムのインスタンスです。[native binary](native-binary.md) はシステムが実行できるファイルであり、process はシステムがそのプログラムを起動したときに実際に動くものです。同じプログラムを二度実行しても、メモリ、開いているファイル、権限は異なる場合があります。

## 例

agent が Lamp のテストランナーを起動すると、OS は `total.c` を開くよう要求できる process を起動します。process は [system call](system-call.md) を使って [kernel](kernel.md) にその操作を要求します。同じランナーでも、sandbox の設定が異なれば、別のファイル群が見える場合があります。

## 重要になる場面

[operating-system process sandbox](operating-system-process-sandbox.md) では、host kernel が実行中の process に制限を適用します。テストランナーは child process と呼ばれる別の process を起動できます。それらにも制限が適用され、必要なデータと開いているファイルだけを引き継ぐことを確認してください。一方、[virtual machine](virtual-machine.md) 内の process は VM 自身の kernel を使います。

ファイルを開く要求の経路は「[Sandbox isolation boundaries](../sandbox-isolation-boundaries.md#follow-a-request-to-open-a-file)」を参照してください。

[用語集に戻る](index.md)
