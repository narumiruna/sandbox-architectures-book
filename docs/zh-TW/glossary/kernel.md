# Kernel

Kernel 是作業系統的核心。它管理 CPU 時間、記憶體、檔案和裝置等資源。程式透過 [system calls](system-call.md) 請它執行操作，例如開啟檔案。

## 範例

同一部 Linux 電腦上的兩個測試 sandbox 可以看見不同的專案目錄，但仍由同一個 Linux kernel 開啟檔案。如果每個 sandbox 改在各自的 [virtual machine](virtual-machine.md) 中執行，每個測試程式就會請自己的 VM kernel，在該 VM 能使用的儲存空間上開啟檔案。

## 哪個 kernel 處理請求？

一般的 [operating-system process sandbox](operating-system-process-sandbox.md) 使用 *host kernel*，也就是底層作業系統的 kernel。Kernel 對這些 processes 套用 [namespaces](namespace.md) 和 [seccomp](seccomp.md) 等控制措施。VM 執行 *guest kernel*，由它管理提供給 VM 的資源。[user-space kernel](user-space-kernel.md) 採用第三種做法：在 host kernel 之外用軟體實作 workload 所使用的 kernel 介面。差異請參閱 [Sandbox 隔離邊界](../sandbox-isolation-boundaries.md)。

[返回詞彙表](index.md)
