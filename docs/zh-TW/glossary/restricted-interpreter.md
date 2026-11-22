# Restricted interpreter

Restricted interpreter 只使用自身實作的語言功能和內建操作來執行程式碼。程式碼只能透過 [host](host.md) 提供的操作與 interpreter 外部互動。語言功能少，不代表權限就小：host 提供的一項操作就可能開放大範圍的存取權限。

## 範例

建置服務讓指令碼使用清單、迴圈和一項 [tool](tool.md)，讀取經核准的建置結果並統計失敗的測試。指令碼無法任意開啟檔案或啟動命令。Tool 傳回任何結果之前，服務仍會確認呼叫者可以讀取所要求的建置結果。

## 支援的語言功能和函式庫

Interpreter 依照自己的規則執行指令碼。Restricted interpreter 可以省略某些語法、內建操作或函式庫支援。程式碼看起來可以像 JavaScript，卻不一定支援一般 JavaScript 環境所提供的套件或操作。這種做法不需要 [WebAssembly](webassembly.md) 或 [engine isolate](engine-isolate.md)。

例如，[OpenCode Code Mode 的 `5310e422` 修訂版](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md)使用 Psychoscript 解譯類似 JavaScript 的語言。該版本不會載入套件，也不允許指令碼直接存取檔案系統、網路或 process。Interpreter 外部的工作由 host 提供的 tool 處理。

## 語言之外的限制

即使支援某種迴圈，它仍可能執行過久；即使核准了 tool 呼叫，它仍可能傳回超出預期的資料。請分別限制執行時間、記憶體和 tool 用量。每項 tool 都應遵循 [least privilege](least-privilege.md)：讀取測試結果的 tool 不應也提供任意執行命令的功能。

[返回詞彙表](index.md)
