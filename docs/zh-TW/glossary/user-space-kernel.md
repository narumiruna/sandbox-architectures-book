# User-space kernel

User-space kernel 是在 [host kernel](kernel.md) 之外處理 workload 的作業系統請求的軟體。它提供程式所需的介面，無須另外啟動 guest kernel。它仍依賴 host kernel 提供資源，而且可能不支援程式預期的所有操作。

## 範例

在使用 gVisor 的建置 sandbox 中，測試程式要求取得自己的 process ID。如 [gVisor 架構指南](https://gvisor.dev/docs/architecture_guide/intro/) 所述，gVisor 的 Sentry 會依自己的 process 記錄回覆，而不會向 host kernel 查詢 sandbox 內程式的 process ID。

## 處理呼叫，而不是篩選呼叫

Sentry 會實作 Linux [system calls](system-call.md)，而不是單純允許或拒絕送往 host 的呼叫。它可以自行向 host kernel 發出範圍更有限的請求；這些請求不必與 workload 的呼叫一一對應。這與共用 kernel 的 [process sandbox](operating-system-process-sandbox.md) 不同，後者由 host kernel 實作 process 獲准發出的呼叫。請測試 workload 所需的介面和效能，不要假設其行為與直接在 Linux 上執行完全相同。

[返回詞彙表](../glossary.md)
