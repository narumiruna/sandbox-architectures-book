# Host function

Host function 是在語言 sandbox 外實作、可由其中的程式碼呼叫的操作。執行 sandbox 的應用程式決定要開放哪些函式。函式以實作它的元件的權限執行，而不只具有呼叫它的指令碼的權限。

## 範例

在 [sandbox](sandbox.md) 內執行的指令碼需要某個專案的版本號碼。應用程式開放一個 host function，從該專案的 manifest 讀取版本，並只傳回版本字串。指令碼不必取得一般的專案檔案存取權，就能取得該值。

## 哪些操作會跨越邊界

語言 runtime 提供呼叫外層應用程式的方法。例如，[WebAssembly](webassembly.md) module 可以呼叫應用程式以 *import* 方式提供的函式，也就是由 module 外部提供的操作。[Wasmtime 安全性文件](https://docs.wasmtime.dev/security.html#webassembly-core) 說明應用程式如何透過明確提供 imports，控制 module 能在自身記憶體之外執行哪些操作。

[Tool](tool.md) 是提供給 agent 或指令碼的操作；host function 是讓語言 sandbox 能呼叫該操作的一種方式。其他 host functions 則提供時鐘之類的基本服務。無論是哪一種，處理程式都必須對輸入、操作產生的影響及傳回的資料強制執行相關 [policy](policy.md)。指令碼本身的限制無法代替這些檢查。

[返回詞彙表](../glossary.md)
