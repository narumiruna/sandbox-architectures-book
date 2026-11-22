# Isolation unit

Isolation unit 是共用同一道 isolation boundary 的一組 workloads，也就是正在執行的工作。邊界在特定層級將不同單位隔開，但本身不會隔開同一單位內的 workloads。

## 範例

一項服務為每個 Kubernetes [pod](pod.md) 提供專屬的 [virtual machine](virtual-machine.md) 作為 sandbox。其中一個 pod 包含測試執行程式和收集結果的輔助程式。它們共用同一個 VM 及其作業系統的 kernel。第二個 pod 使用另一個 VM，因此 VM 邊界隔開的是兩個 pod，而非第一個 pod 裡的兩個程式。

## 這個單位指的是哪一層

[isolation boundary](isolation-boundary.md) 說明工作*如何*隔開；單位則說明每一道邊界會隔開*哪些工作*。若每個 pod 各用一個 VM，單位就是 pod；若每個 container 各用一個 VM，單位就是 [container](container.md)。請參閱[哪些 workloads 共用 guest kernel](../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)中的圖，比較三種實作。

同一個系統可以在另一層有更小的單位。同一個 VM 中的 processes 可以看到不同的檔案系統內容，但這不代表各自有獨立的 guest kernel。如果兩個 [tenants](tenant.md) 不得共用 guest kernel，除了確認服務是否使用 VM，也要確認 [control plane](control-plane.md) 如何安排它們的 workloads。

[返回詞彙表](../glossary.md)
