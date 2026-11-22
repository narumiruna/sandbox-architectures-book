# MicroVM

MicroVM 是一種 [virtual machine](virtual-machine.md)，設計目的是減少啟動和執行所需的工作與資源，通常提供比通用 VM 更少的虛擬裝置。它仍執行自己的作業系統 [kernel](kernel.md)。這個名稱不保證特定的開機時間或安全等級。

## 範例

測試服務為每項工作提供一個 Linux microVM，其中有虛擬磁碟和網路連線，但沒有圖形顯示裝置。這項工作可以執行平常使用的命令列工具。如果 workload 需要 microVM 未提供的裝置，就必須改用其他設定或環境。

## 減少虛擬裝置有什麼影響

MicroVM 的 [virtual machine monitor](virtual-machine-monitor.md) 可以省略目標 workloads 不需要的裝置。例如，[Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/README.md) 省去非必要的裝置和提供給 guest 的功能，以減少額外負擔和 guest 可觸及的程式碼。裝置模型越精簡，對需要其他硬體的 workloads 而言，彈性也越小。

[isolation unit](isolation-unit.md) 取決於服務的設計：一個 microVM 可容納一項工作或多個 workloads。同一個 microVM 裡的 workloads 共用一個 guest kernel。此外，也要確認 sandbox 開放哪些 host 檔案和網路服務；VM 較精簡並不代表它會決定哪些存取可以放行。

[返回詞彙表](index.md)
