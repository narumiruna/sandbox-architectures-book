# WebAssembly {#webassembly}

[WebAssembly (Wasm)](../../glossary/webassembly.md) 讓 [host](../../glossary/host.md) 應用程式執行模組，同時檢查模組的記憶體存取，並明確規定模組能呼叫哪些外部操作。模組不會只因為開始執行，就取得 shell、檔案系統或網路連線。

## 誰處理請求？ {#who-handles-the-request}

程式要求取得 [`LAMP-17`](../../practice/design/from-issue-to-patch.md) 的標題時，Wasm [runtime](../../glossary/runtime.md) 讓模組呼叫應用程式為查詢議題所提供的 [host function](../../glossary/host-function.md)。Host function 會先檢查對該議題的 [authorization](../../glossary/authorization.md)，才傳回標題。標題排序可在模組內完成。

有兩種常見設計會用這個邊界隔離產生的程式碼：

1. **將 workload 當成 Wasm 模組執行。** 應用程式可以把 workload 編譯成 Wasm，再用 [Wasmtime](https://docs.wasmtime.dev/security.html) 等 runtime 執行。模組可以呼叫應用程式提供的 host 操作。
2. **將語言引擎當成 Wasm 模組執行。** 在 [Pi 的 `9c465268` 修訂版本](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) 中，QuickJS 會編譯成 Wasm。模型仍撰寫 JavaScript，由 QuickJS 解譯執行。

## 哪些資源仍會共用？ {#what-stays-shared}

模組可以在同一個 host [process](../../glossary/process.md) 中執行，預設無法存取彼此的記憶體。Host 可以明確將同一項資源（例如議題查詢服務）提供給多個模組。

## 何時適用？ {#when-to-use-it}

如果 workload 或其語言引擎可在 Wasm 中執行，而且不需要一般的 Linux [binaries](../../glossary/native-binary.md)，就選用這種邊界。

## 這個邊界不涵蓋什麼？ {#what-the-boundary-does-not-cover}

記憶體檢查不會限制 host function 代表模組執行的操作。請確認應用程式實際提供哪些操作，不要假定 [WebAssembly System Interface (WASI)](../../glossary/webassembly-system-interface.md) 會授予 host 檔案系統的存取權。也請確認 runtime 如何限制記憶體用量，以及如何停止執行時間過長的程式。

如需了解更多執行 tool 指令碼的方式，請參閱[架構概覽](../../agent-sandbox-architectures.md#code-mode-isolating-tool-scripts-instead-of-shells)。
