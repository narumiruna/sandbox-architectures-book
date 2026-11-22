# Container runtime

Container runtime 是設定並執行 [container](container.md) 的軟體。它會套用選定的隔離設定並啟動程式。兩種 runtime 可以從同一個 [container image](container-image.md) 啟動，但為程式提供不同的隔離界線。

## 範例

建置服務請 runtime 為一項測試工作啟動 sandbox。Runtime 讓專案可在 `/workspace` 使用，並啟動測試執行程式。服務決定何時執行工作以及在哪裡執行；runtime 則設定工作執行的環境。

## 從封裝的檔案到執行中的 process

Container 軟體堆疊可解開 image 內的檔案，加入 runtime 設定以備妥 *bundle*，也就是啟動 workload 所需的本機檔案和設定。[OCI Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/tree/v1.2.1) 定義 bundle 以及建立、啟動等生命週期作業。底層 runtime 可以直接使用已備妥的 bundle，不必自行下載 image。

## Kernel 介面從哪裡來

Runtime 可以搭配 [namespace](namespace.md) 直接使用 host 的 [kernel](kernel.md)，也可以提供 [user-space kernel](user-space-kernel.md)，或在具備自身 kernel 的 [virtual machine](virtual-machine.md) 中執行 workload。[Control plane](control-plane.md) 負責管理 workload；runtime 的執行機制與設定則決定 workload 如何與 host 隔離。

[返回詞彙表](index.md)
