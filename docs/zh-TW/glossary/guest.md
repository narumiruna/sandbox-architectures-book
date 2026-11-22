# Guest

Guest 是在 [virtual machine](virtual-machine.md) 內執行的作業系統和程式。它的 *guest [kernel](kernel.md)* 是該作業系統的核心，負責管理 VM 提供的處理器、記憶體和裝置。它與 [host](host.md) 的作業系統和 kernel 不同。

## 範例

Sandbox 在 Linux guest 內執行測試。當測試開啟檔案時，它會向 guest kernel 提出請求，就像在實體 Linux 電腦上一樣。如果檔案位於以 host 檔案作為儲存後端的虛擬磁碟上，guest 看到的仍然是磁碟，而不是 host 存放該檔案的目錄。

## Guest 控制哪些項目

Guest 程式透過 [system calls](system-call.md) 向 guest kernel 提出請求。Guest kernel 管理 VM 內的程式和檔案。[Hypervisor](hypervisor.md) 和 [virtual machine monitor](virtual-machine-monitor.md) 各自負責提供虛擬硬體的不同部分。例如，[Firecracker v1.11.0 的設計文件](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md) 說明了以 host 檔案作為儲存後端的虛擬區塊裝置。

Guest 內的管理員不會自動取得 host 的管理員權限。不過，任何刻意開放給 guest 的 host 檔案、網路服務或其他資源，都必須有自己的存取控制。同一部 VM 內的 workload 共用 guest kernel；如果這些 workload 必須彼此隔離，請檢查 [isolation unit](isolation-unit.md)。

[返回詞彙表](../glossary.md)
