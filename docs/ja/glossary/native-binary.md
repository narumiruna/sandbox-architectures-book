# Native binary

Native binary は、特定の種類のプロセッサーとオペレーティングシステムのインターフェースに合わせて、命令にコンパイルされたプログラムです。互換性のある実行環境が必要です。Linux の native binary は [WebAssembly](webassembly.md) モジュールではなく、そのまま WebAssembly モジュールとして実行することはできません。

## 例

コードレビュー用の sandbox が、64 ビット Arm Linux 向けにビルド済みの linter を実行します。そのプロセッサーアーキテクチャと必要なライブラリを備えた Linux の [virtual machine](virtual-machine.md) なら実行できます。Wasm runtime で直接動かすには、サービスは Linux の実行ファイルの代わりに Wasm 向けのビルドを用意します。

## 互換性を決めるもの

実行ファイル形式は、プログラムをどう読み込むかをオペレーティングシステムに伝えます。たとえば Linux の [ELF 実行ファイル](https://man7.org/linux/man-pages/man5/elf.5.html) には、対象のプロセッサーアーキテクチャが記録されています。プログラムが共有ライブラリを使う場合は、互換性のある [loader とライブラリ](https://man7.org/linux/man-pages/man8/ld.so.8.html) も必要です。プログラムが使う [system call](system-call.md) は、実行先の kernel インターフェースに対応していなければなりません。プロセッサーが一致するだけでは不十分です。

[用語集に戻る](index.md)
