# Container image

Container image 是一組封裝好的檔案與設定，供 [container runtime](container-runtime.md) 啟動 [container](container.md)。它描述的是啟動時的環境，不是程式正在執行的狀態。

## 範例

建置服務可以重複使用一個包含 Python 直譯器和專案相依項目的 image。每個新的 container 都可以從同一組檔案開始。某次建置寫出的報告不屬於原始 image，除非服務另行儲存或分享報告，否則報告不會出現在其他建置中。

## 封裝的內容

[OCI Image Format v1.1.0](https://github.com/opencontainers/image-spec/blob/v1.1.0/manifest.md) 用 *manifest* 描述 image。Manifest 會參照組態和檔案系統的各個層。組態可以提供預設設定，例如要執行的指令。各個層描述檔案系統的變更，處理 image 的工具會依序套用這些變更，以備妥 container 啟動時使用的檔案。

Image 不會像記憶體 [snapshot](snapshot.md) 那樣保留執行中的 process，也不決定 workload 如何隔離。同一個相容的 image 可以在不同 runtime 下執行。請檢查 runtime 及其 policy，才能知道程式碼能存取哪些資源。

[返回詞彙表](index.md)
