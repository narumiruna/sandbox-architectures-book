# Workload

Workload 是環境為了完成任務而執行的程式碼和 process。在 sandbox 中，它可以是一個指令碼、一項包含多個 process 的建置工作，或整個 agent session。Workload 指實際執行的內容，不是用來啟動它的套件，也不是啟動它的服務。

## 範例

[agent](agent.md) 在一個 [sandbox](sandbox.md) 中執行產生的指令碼，決定要執行哪些測試。接著，tool 在另一個 Linux sandbox 中啟動測試執行器及其輔助 process。指令碼是第一個 workload；測試執行器及其輔助 process 構成第二個。Agent 不必在這兩個 sandbox 中的任何一個執行。

## 為工作選擇隔離邊界

不同的 workload 需要不同的執行環境。彙整多項 tool 結果的指令碼可能只需要 [restricted interpreter](restricted-interpreter.md)。啟動 [native binaries](native-binary.md) 的建置工作需要能執行這些檔案的相容環境，因為這些程式是針對特定機器和作業系統編譯的。

[container image](container-image.md) 提供啟動時使用的檔案和設定，不是執行中的 workload。請確認 workload 的 child processes 實際在哪裡執行、能存取哪些資源，以及多個 workload 是否共用一個 [isolation unit](isolation-unit.md)。請參閱 [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md)，瞭解適合不同工作的環境。

[返回詞彙表](../glossary.md)
