# User space

user space は、アプリケーションや大半のサービスが動く、OS の [kernel](kernel.md) の外側の領域です。user space のプログラムがハードウェアやシステムリソースを直接制御できる範囲は kernel より狭くなります。アプリケーションが user space で動くのは普通で、それだけで sandbox に入っているわけではありません。

## 例

同じ Linux マシンの user space でエディターとテストランナーを動かせます。エディターはユーザーがアクセスできる個人ファイルを読めます。sandbox はテストランナーにプロジェクトの読み取りを許可しますが、個人ファイルの読み取りは許可しません。この制限は user space で動くことではなく、sandbox によるものです。

## プログラムが kernel の機能を要求する方法

ファイルを開くなど kernel の操作が必要なとき、プログラムは多くの場合ライブラリを介して [system call](system-call.md) を行います。「[Linux の system call 入門](https://man7.org/linux/man-pages/man2/intro.2.html)」は、kernel が要求を処理して結果を返す仕組みを説明しています。[user-space kernel](user-space-kernel.md) はそのインターフェースを host kernel の外にあるソフトウェアとして実装します。

[用語集に戻る](../glossary.md)
