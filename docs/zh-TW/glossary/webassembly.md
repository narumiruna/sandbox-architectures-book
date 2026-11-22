# WebAssembly (Wasm)

WebAssembly（縮寫為 Wasm）是一種可跨平台使用的可執行程式碼格式。只要支援程式碼需要的功能，Wasm [runtime](runtime.md) 就能在不同的處理器和作業系統上執行同一份程式碼。Wasm 本身不提供檔案系統、網路連線或 shell。程式碼能存取什麼，取決於 [host](host.md) 提供什麼。

## 範例

記錄服務執行一個 Wasm 模組來統計警告；模組是由指令和資料組成的套件。Host 傳入記錄文字，模組傳回警告數。模組不必自行開啟記錄檔，因此服務不授予它檔案系統存取權。

## 記憶體和 imports

Runtime 建立可執行的模組實例時，會連接模組的 *imports*，也就是模組宣告必須由外部提供的函式或其他資源。[WebAssembly Core Specification 1.0](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#imports) 定義的 imports 可以包含函式，甚至是記憶體。Wasm 讀寫自己的 *linear memory*，也就是實例可使用的一段位元組範圍。[存取超出該範圍](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#memory-instructions) 時，執行會因錯誤而停止，而不是存取 host process 中的其他記憶體。

Runtime 的記憶體檢查不會限制 [host function](host-function.md) 的作用。即使呼叫者無法直接讀取檔案，讀取檔案的函式仍須強制執行自己的存取規則。Host 可以提供自訂函式，也可以提供 [WebAssembly System Interface (WASI)](webassembly-system-interface.md) 等標準介面。要在其他地方執行模組，請確認新環境支援所需的 Wasm 功能和 imports。

## 哪些程式碼會編譯成 Wasm？

Workload 可以是 Wasm 模組，也可以由作為 Wasm 模組的語言引擎執行。[Pi `codemode` 的 `9c465268` 修訂版](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) 將 QuickJS 編譯成 Wasm，並為它所執行的 JavaScript 提供 tool。引擎是 Wasm 模組；指令碼仍然是 JavaScript。光看相依套件的名稱 [`quickjs-wasi`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/package.json)，無法得知指令碼取得哪些存取權限。

## 何時使用

如果程式碼只需要選定的 host 操作，不需要完整的作業系統，可以考慮使用 Wasm。一般 Linux [native binary](native-binary.md) 無法直接當成 Wasm 模組執行。請參閱[基礎篇的 WebAssembly](../isolation/generated-scripts/webassembly.md)，其中有查詢 tool 的範例。

[返回詞彙表](index.md)
