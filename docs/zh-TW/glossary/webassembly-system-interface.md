# WebAssembly System Interface (WASI)

[WebAssembly System Interface (WASI)](https://wasi.dev/) 是一組標準介面，host 可以透過它們讓 [WebAssembly](webassembly.md) 程式讀取檔案、查詢時間等。WASI 說明如何要求這些服務。它不是作業系統，支援某個介面並不表示程式可以存取該介面能描述的所有資源。

## 範例

Sandbox 透過 WASI 授予報告產生器某個測試結果目錄的唯讀存取權。報告產生器不用取得 host 的整個檔案系統，也能讀取這些結果。它無法透過取得的唯讀權限寫入該目錄。

## 介面和權限

Wasm 程式將它需要的介面宣告為 imports，也就是對必須從程式外部提供的函式或資源提出的要求。Host 決定透過這些介面授予哪些存取權限。例如，在 WASI 0.2.0 中，[filesystem preopens 介面](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/filesystem/preopens.wit) 會列出程式在啟動時獲准存取的目錄。[檔案系統型別](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/filesystem/types.wit) 要求路徑不能超出 *handle* 所識別的目錄；handle 是用來提出檔案系統請求的參照。存取旗標可以阻止透過該 handle 進行變更。

請檢查實際授予的權限，不要只看介面名稱。程式也可能取得自訂的 [host functions](host-function.md)，藉此在 WASI 之外存取資源。這些函式需要各自檢查權限。

## 版本與作業系統相容性

[WASI Preview 1](https://wasi.dev/releases/wasi-p1) 使用名稱為 `wasi_snapshot_preview1` 的核心 Wasm 模組 imports。[WASI 0.2 (Preview 2)](https://github.com/WebAssembly/WASI/blob/v0.2.0/preview2/README.md) 使用 WebAssembly Component Model，透過 WIT 描述的介面連接 Wasm 元件。WIT 是一種用於命名函式及其資料型別的語言。請確認 [runtime](runtime.md) 和 host 提供的版本和介面符合程式的需求。WASI 不提供 Linux kernel，也不能讓一般 Linux [native binary](native-binary.md) 當成 Wasm 執行。

[返回詞彙表](../glossary.md)
