# Extended Page Tables (EPT)

Extended Page Tables（EPT）を使うと、[Intel のプロセッサー](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)は、[guest](guest.md) から物理アドレスに見えるメモリーアドレスを、[host](host.md) の物理アドレスに変換できます。これはアドレス変換の第 2 段階です。ページテーブルには、メモリー領域がどこに対応するかと、どの種類のアクセスを許可するかが記録されます。

## 例

アプリが仮想アドレスからデータを読み込みます。Guest のページテーブルは、その仮想アドレスを Guest の物理アドレスに対応付けます。次に CPU が EPT を使い、対応する Host の物理アドレスを見つけます。Guest kernel は自身のページテーブルを変更できますが、EPT は制御しません。別の Guest は、Host の同じメモリーを使うことなく、同じ Guest 物理アドレスを使えます。

## 第 2 段階の対応付けを制御する主体

Linux Host が [KVM](kernel-based-virtual-machine.md) を使う場合、第 2 段階の対応付けは KVM が設定します。Guest の実行中は、CPU がそのアクセス権限を適用します。KVM が対応するアドレス変換については、[KVM のメモリーに関するドキュメント](https://docs.kernel.org/virt/kvm/x86/mmu.html#translation)を参照してください。

[用語集に戻る](index.md)
