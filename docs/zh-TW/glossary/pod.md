# Pod

Pod 是 Kubernetes 可部署的最小單位。它包含一或多個一起執行的 [containers](container.md)，這些 containers 共用網路環境，也可以共用儲存空間。Pod 不一定有自己的 kernel：[isolation boundary](isolation-boundary.md) 由所選的 runtime 決定。

## 範例

測試 sandbox 在同一個 pod 的兩個 containers 中，分別執行網頁伺服器與測試執行程式。測試執行程式可以透過 `localhost` 連線到伺服器。如果服務在兩個 containers 中都掛載同一個輸出目錄，兩者都能讀取儲存在該處的測試結果。

## 共用 pod 代表什麼

在 [Kubernetes Pods 文件](https://kubernetes.io/docs/concepts/workloads/pods/)所述的標準模型中，同一個 pod 中的 containers 共用 IP 位址和連接埠空間。哪些 containers 需要共用儲存空間，就必須為它們設定。使用 [virtual machine](virtual-machine.md) 的 runtime 可以把 pod 當成 [isolation unit](isolation-unit.md)。例如，[Kata Containers 4.4.0](https://github.com/kata-containers/kata-containers/blob/4.4.0/docs/design/architecture/README.md#kubernetes-support) 將 Kubernetes pod 放在一個 VM 中。其中的 containers 共用該 VM 的 guest kernel，而不是各有一個 VM。這與每個 container 各用一個 VM 有何差異，請參閱[哪些 workloads 共用 guest kernel（英文）](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)。

[返回詞彙表](../glossary.md)
