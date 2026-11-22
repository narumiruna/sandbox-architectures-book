# Tool

Tool 是 agent 或指令碼可以要求執行的操作，例如查詢議題或啟動建置。呼叫者提供輸入，由稱為 handler 的元件執行操作。允許呼叫某個 tool，不代表應該允許送給它的每一個請求。

## 範例

發行指令碼在 [sandbox](sandbox.md) 中執行，並呼叫 tool 取得議題標題。指令碼提供議題編號。Handler 確認該議題屬於指令碼有權讀取的專案後，只傳回標題。Handler 可以使用議題服務，而不必把自己的 [credential](credential.md) 交給指令碼。

## 介面與 handler

Tool 介面說明呼叫者可以提出哪些請求。在語言 sandbox 中，[host function](host-function.md) 可以讓指令碼將請求送給 handler。Handler 強制執行 [policy](policy.md)：先確認呼叫者能否對該資源執行操作，再將影響和結果限制在獲准範圍內。議題編號的格式正確，並不代表呼叫者有權讀取該議題。

Sandbox 可以限制指令碼能呼叫哪些 tool，但無法將指令碼受到的限制套用到在外部執行的 handler。建置 tool 可以在適合該 [workload](workload.md) 的另一個 sandbox 中啟動工作。此時，指令碼邊界和建置邊界各自保護系統的不同部分。

[返回詞彙表](../glossary.md)
