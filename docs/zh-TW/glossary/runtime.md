# Runtime

Runtime 是執行程式碼或為程式碼準備執行環境的軟體。僅憑這個名稱，無法得知它能執行哪類程式碼，或用什麼方式將程式碼與其他程式隔開。

## 範例

Agent 服務在可存取測試結果的 sandbox 中，執行已編譯成 [WebAssembly](webassembly.md) 的報告產生器。需要執行新測試時，服務透過 [container runtime](container-runtime.md) 啟動建置用的 container。Wasm runtime 執行報告產生器；container runtime 則為原生測試程式準備環境。

## Runtime 執行或準備什麼

語言 runtime 可以用語言引擎或 [restricted interpreter](restricted-interpreter.md) 執行指令碼。Wasm runtime 載入並執行模組；模組是由 Wasm 指令和資料組成的套件。Runtime 建立可執行的模組實例時，應用程式可以提供選定的 [host functions](host-function.md)。Container runtime 則為 process 設定檔案系統和其他資源。例如，[OCI Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/blob/v1.2.1/runtime.md#lifecycle) 說明如何在啟動程式之前，依據設定建立 container 環境。

## 管理不等於隔離

[control plane](control-plane.md) 可以決定何時及在哪裡啟動 sandbox，runtime 則負責執行程式碼或準備環境。同一個產品可以同時負責兩者。要辨識 [isolation boundary](isolation-boundary.md)，請確認哪個元件強制執行隔離，以及 workload 可以使用哪些 host 資源。例如，container runtime 可以啟動共用 host kernel 的 process，也可以將它們放在有獨立 kernel 的 VM 內。

[返回詞彙表](index.md)
