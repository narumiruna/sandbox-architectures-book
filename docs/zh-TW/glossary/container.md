# Container

Container 是為一或多個程式準備的執行環境。它提供檔案系統和一組資源供這些程式使用。光看 *container* 這個詞，無法判斷程式和 host 之間如何隔離。

## 範例

程式碼審查服務會啟動一個 container，其中包含專案所需的編譯器和測試工具。第二項測試工作可以從同一個 [container image](container-image.md) 啟動自己的 container。Image 提供啟動時的檔案；每個執行中的 container 都有自己的測試 process，也可能有獨立的可寫入檔案系統。

## 隔離由何處提供

[Container runtime](container-runtime.md) 會設定執行環境。若共用 kernel，Linux 的 [namespace](namespace.md) 可以讓各個 process 看到不同的資源，而 [control group](control-group.md) 可以統計或限制資源用量。Runtime 也可以用 [user-space kernel](user-space-kernel.md) 隔離 container，或在 [virtual machine](virtual-machine.md) 中執行 container。這些方法可以使用同一個 image 啟動，但有不同的 [isolation boundary](isolation-boundary.md)。

請檢查 runtime 與 workload 共用哪些資源。例如，不論 container 如何封裝，來自 host 的可寫入 [mount](mount.md) 都可能讓程式碼變更 host 檔案。請參閱 [VM、container 與 microVM 的比較](../sandbox-isolation-boundaries.md#compare-a-vm-a-container-and-a-microvm)。

[返回詞彙表](index.md)
