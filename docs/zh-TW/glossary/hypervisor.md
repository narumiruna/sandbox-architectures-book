# Hypervisor

Hypervisor 是一種軟體，控制 [virtual machines](virtual-machine.md) 如何使用實體電腦的處理器和記憶體。有些專案交替使用 *hypervisor* 和 *virtual machine monitor* 這兩個術語。本書以 [virtual machine monitor (VMM)](virtual-machine-monitor.md) 指稱管理 VM 及其虛擬裝置的元件。

## 範例

一部伺服器在不同的 VM 中執行兩個測試 sandbox。每個 VM 都只看得到自己的虛擬處理器和記憶體。Hypervisor 讓兩個 VM 共用同一部實體電腦，但不讓任何一方直接存取另一方的記憶體。

## 虛擬執行與存取規則

有硬體支援的 hypervisor 使用處理器功能來執行 guest 指令，並限制 guest 可存取的實體記憶體。VMM 可以透過 [KVM](kernel-based-virtual-machine.md) 等 host 介面設定執行環境，並提供 guest 程式所需的裝置行為。比較 [Linux KVM API](https://docs.kernel.org/virt/kvm/api.html) 和 [Microsoft Hypervisor 規格](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/tlfs)，可了解這些職責如何透過兩種不同方式提供給上層使用。

是否讓 sandbox 看見專案目錄或連線到外部服務，並非由 hypervisor 決定。這取決於周邊系統開放哪些資源，以及它如何強制執行 [policy](policy.md)。

[返回詞彙表](../glossary.md)
