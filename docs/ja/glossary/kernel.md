# Kernel

Kernel は、オペレーティングシステムの中核です。CPU 時間、メモリー、ファイル、デバイスなどのリソースを管理します。ファイルを開くときなど、プログラムは [system call](system-call.md) を通じて kernel に処理を依頼します。

## 例

同じ Linux マシン上の 2 つのテスト用 sandbox は、それぞれ異なるプロジェクトディレクトリを参照しながら、同じ Linux kernel にファイルを開くよう依頼できます。一方、各 sandbox が専用の [virtual machine](virtual-machine.md) で実行される場合は、各テストプログラムが自分の VM の kernel に、その VM が利用できるストレージ上のファイルを開くよう依頼します。

## どの kernel がリクエストを処理するか

通常の [operating-system process sandbox](operating-system-process-sandbox.md) は、基盤となるオペレーティングシステムの kernel、つまり *host kernel* を使います。Kernel は、それらの process に [namespace](namespace.md) や [seccomp](seccomp.md) などの制御を適用します。VM では、VM に提供されたリソースを管理する *guest kernel* が動きます。[User-space kernel](user-space-kernel.md) は第 3 の方法で、workload が使う kernel インターフェースを host kernel の外にあるソフトウェアとして実装します。違いについては [Sandbox の isolation boundary](../sandbox-isolation-boundaries.md) を参照してください。

[用語集に戻る](index.md)
