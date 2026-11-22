# Agent

Agent 是一種使用 AI 模型來決定下一步、並可呼叫工具來執行動作的系統。Agent 可以請模型編寫指令碼，但該指令碼只是 agent 可能執行的其中一項工作。把指令碼放進 sandbox，並不會把 agent 的其餘部分也放進同一個 sandbox。

## 範例

某個 agent 要準備專案進度報告。它請模型編寫指令碼，查詢議題標題並依標籤分組。指令碼在 [sandbox](sandbox.md) 內執行，而且只能呼叫查詢議題的 [tool](tool.md)。呼叫模型的應用程式和處理議題查詢的服務都在該指令碼的 sandbox 外執行。

## Agent 會執行什麼

Agent 可以交付任務給模型、執行模型要求的工具，再把結果傳回模型，供模型決定下一步。它可以一次要求呼叫一個工具，也可以用 [Code Mode](code-mode.md) 讓產生的指令碼呼叫多個工具並彙整結果。

另一種設計則把 agent 應用程式本身和它啟動的本機指令都放在 sandbox 內執行。要區分這兩種設計，可以問：在每個 [isolation boundary](isolation-boundary.md) 中，哪些程式碼是 [workload](workload.md)？界線外的工具處理程式使用自己的權限，即使請求來自界線內也一樣。

[返回詞彙表](../glossary.md)
