# Restricted interpreter {#restricted-interpreters}

[Restricted interpreter](../../glossary/restricted-interpreter.md) 只支援自己實作的語言功能和內建操作。指令碼若能呼叫額外的操作，這些操作都由 [host](../../glossary/host.md) 提供。即使語言名稱很熟悉，也不代表能使用平常用的函式庫或系統 API。

## 誰處理請求？ {#who-handles-the-request}

指令碼要求取得 [`LAMP-17`](../../practice/design/from-issue-to-patch.md) 的標題時，直譯器會執行指令碼，但把查詢交給 host 的 [tool](../../glossary/tool.md) 處理。Tool 會先檢查對該議題的 [authorization](../../glossary/authorization.md)，才傳回標題。迴圈和排序在直譯器內執行。指令碼不需要議題追蹤系統的函式庫，也不需要直接存取網路。

[OpenCode 的 `5310e422` 修訂版本](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md) 使用 Psychoscript 支援 JavaScript 的部分功能。[Pydantic AI Code Mode](https://pydantic.dev/docs/ai/harness/code-mode/) 使用 [Monty（此處為 `5f4a3dfc` 修訂版本）](https://github.com/pydantic/monty/blob/5f4a3dfc493538bb9dc319974393391ba9e7cf14/README.md) 支援 Python 的部分功能。兩者都能讓產生的程式碼呼叫 tool，而不必提供完整的語言環境。

## 哪些資源仍會共用？ {#what-stays-shared}

直譯器可以在 host 應用程式的 [process](../../glossary/process.md) 中執行。限制語言功能本身不會分隔作業系統，也不會讓每份指令碼各有一個 process。不同的指令碼也可使用相同的 host tool。

## 何時適用？ {#when-to-use-it}

如果指令碼主要用來組合 tool 呼叫並處理結果，就選用這種邊界。請用模型可能產生的程式碼來測試：簡短且有效的 Python 或 JavaScript 程式碼，仍可能使用支援範圍以外的功能或函式庫。

## 這個邊界不涵蓋什麼？ {#what-the-boundary-does-not-cover}

即使指令碼無法直接存取檔案，只要能呼叫不受限制的寫入 tool，仍能修改 host 檔案。請另外檢查 host tool。也請確認直譯器如何停止執行時間過長的指令碼，因為即使迴圈受到支援，也可能跑得太久。
