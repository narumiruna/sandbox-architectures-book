# Virtual machine (VM)

Virtual machine（VM）是一種運算環境，會向自己的作業系統提供虛擬處理器、記憶體和裝置。該作業系統有自己的 [guest kernel](guest.md)。由硬體支援的 VM 使用處理器功能隔離 guest 與 [host](host.md) 的執行，但 sandbox 仍可讓 guest 存取選定的 host 資源。

## 範例

建置服務將兩項工作放在不同的 Linux VM 中執行。兩項工作都能在各自的 guest 檔案系統中安裝套件。如果服務讓兩台 VM 都透過可寫入的 [mount](mount.md) 存取同一個 host 目錄，兩項工作仍然能影響對方在該目錄使用的檔案。

## VM 隔離什麼

在 VM 內，程式向 guest kernel 要求開啟檔案之類的服務。[hypervisor](hypervisor.md) 控制底層 CPU 和記憶體的使用，而 [virtual machine monitor](virtual-machine-monitor.md) 管理 VM 和它的虛擬裝置。請參閱 [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md#1-hardware-backed-virtual-machines)，瞭解這和在 host kernel 上執行 process 有何不同。

一台 VM 可以執行一個 workload，也可以容納多個 [containers](container.md)。這些 container 可以各有獨立的檔案系統，但仍共用 guest kernel。請確認哪些工作負載有自己的 VM，以及外層 sandbox 開放哪些磁碟、mount 和網路連線。

[返回詞彙表](index.md)
