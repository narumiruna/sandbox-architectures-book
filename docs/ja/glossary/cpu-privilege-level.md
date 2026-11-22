# CPU privilege level

CPU privilege level は、コードがプロセッサー上でどの操作を直接実行できるかを決めます。x86-64 では通常、[operating-system kernel](kernel.md) は最も特権の高い ring 0 で動き、アプリケーションは ring 3 の [user space](user-space.md) で動きます。アプリケーションは [system call](system-call.md) を使うことで、ring 0 の特権を得ずに Kernel へ操作を要求できます。

## 例

Linux アプリケーションがファイルを開くとき、プロセッサーは ring 3 から ring 0 に切り替わり、Kernel の System call ハンドラーの実行を始めます。Kernel は要求を確認し、ring 3 のアプリケーションに結果を返します。

## Guest 内の特権

[Intel VT-x](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) は、[guest](guest.md) の実行（VMX non-root operation）と [host](host.md) の実行（VMX root operation）を分けます。どちらでも ring 0 と ring 3 を使えます。ring 0 の Guest kernel は自身のアプリケーションより高い特権を持ちますが、実行は Guest 側のままです。Guest の ring 3 から同じ Guest の ring 0 に移っても、[VM exit](vm-exit.md) にはなりません。

[用語集に戻る](../glossary.md)
