# System call (syscall)

system call（syscall）は、プログラムが OS の [kernel](kernel.md) に送る要求です。ファイルを開く、process を起動する、ネットワークソケットでデータを送るといった操作がその例です。

## 例

ビルド用 sandbox のコンパイラが `/workspace/main.c` を開くよう要求します。kernel を共有する sandbox では、host kernel がコンパイラから見える mount 済みのファイルシステムを使ってパスを解決し、ファイルを開けるかを確認します。アクセスが拒否されると要求は失敗します。

## 要求の処理方法

「[Linux の system call 入門](https://man7.org/linux/man-pages/man2/intro.2.html)」にあるように、プログラムは多くの場合、実際の system call を行うライブラリ関数を呼び出します。kernel を共有する sandbox では host kernel が呼び出しを処理し、[seccomp](seccomp.md) でフィルタリングできます。[virtual machine](virtual-machine.md) では guest kernel が内部のプログラムからの呼び出しを処理します。[user-space kernel](user-space-kernel.md) は各要求を host kernel に直接転送せずに同じインターフェースを実装できます。

[用語集に戻る](../glossary.md)
