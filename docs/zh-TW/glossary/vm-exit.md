# VM exit

VM exit 是處理器從執行 [guest](guest.md) 切換到執行其 [hypervisor](hypervisor.md) 的過程。VM exit 不會關閉 [virtual machine](virtual-machine.md)。Hypervisor 可以處理這個事件，再恢復執行 guest。

## 範例

Guest 的驅動程式存取虛擬裝置。如果該存取操作設定為觸發 VM exit，在使用 KVM 的 Linux host 上，CPU 就會把控制權交給 [KVM](kernel-based-virtual-machine.md)。KVM 可以在 host kernel 中處理事件，或把控制權交還給 [virtual machine monitor (VMM)](virtual-machine-monitor.md)，由它提供裝置的運作行為。

## 與 guest system call 的差異

[system call](system-call.md) 通常會將 [privilege level](cpu-privilege-level.md) 從 guest 應用程式切換到 guest kernel，而不離開 guest。VM exit 則會跨越 guest 的邊界。在 KVM 上，這也不同於 host 的 [`KVM_RUN`](https://docs.kernel.org/virt/kvm/api.html#kvm-run) 呼叫返回 VMM：有些 exit 處理完成後，不須等該呼叫返回，就能繼續執行 guest。

[返回詞彙表](index.md)
