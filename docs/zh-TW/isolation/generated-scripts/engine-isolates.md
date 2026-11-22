# Engine isolate {#engine-isolates}

[Engine isolate](../../glossary/engine-isolate.md) 在 [V8](https://github.com/v8/v8/blob/13.8.258/include/v8-isolate.h#L277-L285) 等語言引擎內，將指令碼的物件和執行狀態彼此隔離。由嵌入該引擎的平台決定程式碼可以使用哪些 API。

## 誰處理請求？ {#who-handles-the-request}

指令碼要求取得 [`LAMP-17`](../../practice/design/from-issue-to-patch.md) 的標題時，引擎會執行指令碼，平台則透過具名連線把請求送到議題服務。議題服務會先檢查對該議題的 [authorization](../../glossary/authorization.md)，才傳回標題。

[Cloudflare Dynamic Workers](https://blog.cloudflare.com/dynamic-workers/) 為 JavaScript 提供這類執行環境。在 Cloudflare 文件的範例中，呼叫端可以用 `globalOutbound: null` 阻擋一般的對外請求，同時仍可提供特定的 **binding**，也就是通往另一項服務的具名連線。

## 哪些資源仍會共用？ {#what-stays-shared}

即使引擎會分隔指令碼的狀態，不同 isolate 仍可共用同一個作業系統 [process](../../glossary/process.md)。平台也可以把多個 isolate 連到同一項服務。Isolate 不是獨立的 process，也不是 [VM](../../glossary/virtual-machine.md)。

## 何時適用？ {#when-to-use-it}

如果指令碼需要語言引擎的功能和少數平台 API，但不需要 shell 或原生套件，就選用這種邊界。

## 這個邊界不涵蓋什麼？ {#what-the-boundary-does-not-cover}

即使指令碼不能直接發出網路請求，只要某個 binding 能從任意 URL 取得資料，就等於開放了廣泛的存取權。請一併檢查 worker 的 binding 和預設網路存取權。也請確認哪些指令碼共用同一個 process，以及平台對引擎還施加了哪些其他限制。
