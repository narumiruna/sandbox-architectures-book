# Sandbox Architectures Book

[Sandbox](glossary/sandbox.md) 讓程式在存取受限的環境中執行。本書說明 sandbox 如何強制執行這些限制，以及如何為你要執行的程式碼選擇適合的邊界。

只呼叫幾個 API 的 AI agent，和需要安裝套件、建置軟體、執行測試的 agent，所需的環境不同。選擇時應先看 agent 必須完成哪些工作，而不是先挑產品。

## 從這裡開始 {#start-here}

先閱讀**基礎概念**，再跟著 Lamp 這個虛構的程式開發任務，從第一次執行一路看到如何把它做成供不同客戶使用的服務。如果你已經熟悉隔離機制，可以直接從**設計 sandbox** 的完整範例開始。

1. **基礎概念。** [Sandbox 的隔離邊界](sandbox-isolation-boundaries.md)說明由什麼機制強制執行存取限制。認識六種方式，用來執行作業系統上的 workload，或在程式語言或模組的 runtime 中執行程式碼。
2. **設計 sandbox。** [從問題單到修補程式（英文）](../practice/design/from-issue-to-patch.md)追蹤 Lamp 從查詢問題單到人工審查的資料流向與權限變化。接著[選擇 sandbox（英文）](../practice/design/choosing-a-sandbox.md)，並決定[在哪裡執行、由誰營運（英文）](../practice/design/deployment-patterns.md)。
3. **設定存取規則。** 從 [tool authorization（英文）](../practice/design/tool-authorization.md)開始，接著決定任務的各個環節可以使用哪些檔案、網路端點和憑證。將不同客戶或團隊的工作與資料分開。
4. **營運 sandbox。** 先閱讀 [control plane（英文）](../practice/operations/control-planes.md)，了解由誰啟動及清理 worker，再學習如何管理 worker 的存續時間、限制資源用量，以及診斷故障。
5. **驗證 sandbox。** 先[確認存取規則有效（英文）](../practice/verification/verifying-access-rules.md)，再[量測任務表現（英文）](../practice/verification/measuring-a-sandbox.md)。本機實驗用來示範方法，不代表正式環境的安全性或執行速度。
6. **擴充 sandbox 服務。** 用兩個測試客戶[演練 Lamp 遷移（英文）](../practice/operations/scaling-a-sandbox.md)。確認你需要更多 worker、不同的隔離方式，還是兩者都需要。

## 善用參考資料 {#use-the-reference}

- [Agent sandbox 架構（英文）](../agent-sandbox-architectures.md)比較實際的實作方式。確認 workload 所需的邊界後，可以用這份比較找出候選方案。
- [術語表](glossary.md)定義不熟悉的術語，並連結到詳細說明。

## 閱讀本書時要思考的問題 {#questions-to-carry-through-the-book}

1. **必須隔離什麼？** 是呼叫 tool 的指令碼、一個 process，還是整個 Linux workspace？
2. **什麼可以跨越邊界？** Workload 可以存取哪些檔案、網路端點、憑證和 tool？
3. **執行結束後會留下什麼？** 哪些資料會留在 workspace、snapshot 或快取中？
