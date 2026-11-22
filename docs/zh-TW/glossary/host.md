# Host

Host 是位於 [sandbox](sandbox.md) 外、為它提供資源的系統。對 [virtual machine](virtual-machine.md) 而言，這通常指執行 VM 的機器或作業系統。對語言 sandbox 而言，則可以指執行指令碼引擎的應用程式。*Host* 指的是相對於某個特定邊界的角色。

## 範例

建置服務在一部伺服器上執行 Linux [guest](guest.md)。Host 提供 CPU 時間和記憶體，並使用檔案作為 VM 磁碟的儲存後端。團隊選擇透過唯讀 [mount](mount.md) 開放專案目錄，讓建置工作可以讀取原始碼，但不能變更 host 上的副本。

## 資源與存取

Host 端負責建立邊界，並提供跨越邊界的方式。VM 可以取得虛擬磁碟及網路連線。指令碼 sandbox 可以取得能讀取單一專案檔案的 [host function](host-function.md)。這些選擇會影響 workload 能執行哪些操作；有邊界並不代表廣泛授予資源存取權就是安全的。

Host 不一定是 [control plane](control-plane.md)。Control plane 可以決定 sandbox 放在哪裡，再由另一部機器執行它。設計中提到「host」時，請辨識所指的邊界，以及實際提供資源的元件。

[返回詞彙表](index.md)
