# Code Mode

Code Mode 是一種讓模型編寫程式來呼叫工具並彙整結果的模式。這個術語描述的是模型如何使用工具，而不是程式如何與系統其餘部分隔離。即使程式在 sandbox 內執行，工具處理程式和 agent 的其餘部分仍可能在 sandbox 外執行。

## 範例

某個 [agent](agent.md) 需要列出仍有未關閉議題的里程碑。它不為每次議題查詢分別詢問模型，而是在 [sandbox](sandbox.md) 中執行一份產生的指令碼。指令碼針對每個里程碑呼叫議題查詢工具、統計結果，並傳回簡短摘要。Agent 可以用這份摘要來決定下一步。

## 執行產生的程式

應用程式會選擇指令碼可呼叫的工具，以及執行指令碼的 [runtime](runtime.md)。例如，[本書所涵蓋修訂版本的 Pi `codemode`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) 使用編譯成 [WebAssembly](webassembly.md) 的 QuickJS 來執行 JavaScript，並開放應用程式提供的工具供指令碼使用。[Restricted interpreter](restricted-interpreter.md) 也可以在不使用 Wasm 的情況下執行 Code Mode。

## 檢查工具呼叫

指令碼的執行界線可以限制它能使用哪些工具。每個 [tool](tool.md) 的處理程式仍須檢查是否允許請求的動作。即使指令碼無法直接存取網路，議題查詢也應檢查專案。其他實作方式請參閱[架構綜覽（英文）](../../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells)。

[返回詞彙表](../glossary.md)
