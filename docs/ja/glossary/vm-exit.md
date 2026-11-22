# VM exit

VM exit は、[guest](guest.md) の実行から、その [hypervisor](hypervisor.md) の実行へとプロセッサが切り替わることです。VM exit は [virtual machine](virtual-machine.md) を停止するわけではありません。hypervisor はイベントを処理し、guest を再開できます。

## 例

guest のドライバーが仮想デバイスにアクセスします。そのアクセスで VM exit が起こるように設定されている場合、CPU は Linux KVM host 上の [KVM](kernel-based-virtual-machine.md) に制御を渡します。KVM は host kernel 内でイベントを処理するか、デバイスの動作を提供する [virtual machine monitor (VMM)](virtual-machine-monitor.md) に制御を戻します。

## guest の system call との違い

[system call](system-call.md) は通常、guest の外に出ずに、guest アプリから guest kernel へ [privilege level](cpu-privilege-level.md) を切り替えます。一方、VM exit は guest の境界を越えます。KVM では、host の [`KVM_RUN`](https://docs.kernel.org/virt/kvm/api.html#kvm-run) 呼び出しが VMM に戻ることとも異なります。一部の exit は、その呼び出しが戻らないまま処理され、guest の実行が再開します。

[用語集に戻る](index.md)
