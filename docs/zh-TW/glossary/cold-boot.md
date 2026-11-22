# Cold boot

Cold boot 透過開機啟動新 [virtual machine](virtual-machine.md) 內的作業系統，而不是從已儲存的執行狀態接續執行。它可以使用預先準備的磁碟映像檔，不需要從頭安裝作業系統。

## 範例

建置服務從已包含編譯器的磁碟映像檔啟動 Linux sandbox。Linux 在 VM 內啟動，VM 內的一項服務也開始接受建置指令。沒有任何編譯器 process 或其他執行中的程式從先前的 VM 延續下來。

## 從開機到 sandbox 就緒

[Virtual machine monitor](virtual-machine-monitor.md) 會設定虛擬硬體。[Guest](guest.md) 的 kernel 啟動後，guest 會啟動自己的程式與服務。[修訂版本 `42f413d` 的 NVX 程式庫指南](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/library.md#cold-boot) 示範 cold boot，並將[從已儲存的記憶體和 VM 狀態還原](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/library.md#restore-from-a-snapshot)說明為另一條路徑。

請分開量測開機和就緒時間。Guest 開機完畢時，sandbox 可能還沒接上專案的 workspace，也可能還無法執行第一道指令。[Cold start](cold-start.md) 可以包含 cold boot，也可以使用 [snapshot](snapshot.md) 跳過 guest 開機。

[返回詞彙表](../glossary.md)
