# Sandbox session

Sandbox session 是 [sandbox](sandbox.md) 服務當作一個單位追蹤的一次執行或一段使用期間。服務可以在同一個 session 中保留 [workspace](workspace.md) 和 worker 狀態，供多個請求使用。

## 範例

一個 Lamp session 包含兩個請求：先編輯原始碼，再執行測試。在 session 期間，測試執行器可以看到編輯後的變更。服務關閉 session 時，可以捨棄 workspace，並將測試報告保留為 [artifact](artifact.md)。

## 何時需要留意

多個請求共用同一個 session 時，請確認暫停、恢復和清理後會保留哪些檔案和狀態。關閉 session 可以停止命令並釋出 worker，卻不一定會刪除另行儲存的輸出。

請參閱 [sandbox 生命週期（英文）](../../practice/operations/sandbox-lifecycle.md)。
