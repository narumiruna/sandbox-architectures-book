# Virtual machine monitor (VMM)

Virtual machine monitor（VMM）是建立或管理 [virtual machine](virtual-machine.md) 並提供其虛擬裝置的軟體。有些專案稱這種軟體為 [hypervisor](hypervisor.md)。本書用 *VMM* 表示負責管理 VM 和裝置的軟體，而不是整個 sandbox 服務或 VM 內執行的作業系統。

## 範例

測試服務啟動一台 VM，並要求 VMM 掛接虛擬磁碟。VM 內的程式向 [guest kernel](guest.md) 要求讀取檔案。VMM 提供虛擬磁碟的運作行為，不會直接接收這些程式發出的 guest system calls。

## 位於 host 介面和 guest 之間

對於由硬體支援的 VM，VMM 透過 host 的虛擬化介面來設定 guest 記憶體和虛擬處理器。它也提供或連接 guest 所見的虛擬裝置。例如，[Firecracker v1.11.0 的設計文件](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md) 說明如何用 [KVM](kernel-based-virtual-machine.md) 執行虛擬處理器，以及如何提供以 host 檔案為底層儲存的虛擬磁碟。

Sandbox 的 [control plane](control-plane.md) 可以用 VMM 啟動和停止 VM，但決定工作在哪裡執行，以及誰能存取 workspace 或網路，是不同的職責。要瞭解 sandbox 開放了什麼，請檢查整個 sandbox，而不只是 VMM。

[返回詞彙表](../glossary.md)
