# 使用硬體輔助虛擬化的 VM {#hardware-backed-virtual-machines}

[Virtual machine (VM)](../../glossary/virtual-machine.md) 讓 [agent](../../glossary/agent.md) 在有自己作業系統 [kernel](../../glossary/kernel.md) 的電腦環境中工作。環境內的程式不會直接向 [host](../../glossary/host.md) kernel 發出作業系統請求。

## 誰處理請求？ {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md) 的測試執行程式透過 [system call](../../glossary/system-call.md) 要求開啟 `total.c` 時，由 [guest kernel](../../glossary/guest.md) 處理。這個 kernel 會在 guest 的檔案系統中查找該路徑。如果專案放在虛擬磁碟或共用目錄中，guest 就能從該處讀取專案。能執行一般 Linux 指令，不代表 guest 就能開啟 host 上的任意檔案。

[Virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md) 管理 VM 和 guest 看得到的裝置。例如，[Firecracker 的 `58cf1b2c` 修訂版本](https://github.com/firecracker-microvm/firecracker/blob/58cf1b2cdca407f2323d1b0b25ebb95dfe5b4bcb/docs/design.md) 向 Linux guest 提供虛擬磁碟和網路裝置。[MicroVM](../../glossary/microvm.md) 通常比通用型 VM 開放更少裝置，但仍有自己的 guest kernel。若要對照各種邊界和取捨，請參閱 [VM、container 和 microVM 的比較](../../sandbox-isolation-boundaries.md#compare-a-vm-a-container-and-a-microvm)。

## 哪些資源仍會共用？ {#what-stays-shared}

同一台 VM 裡的兩個 [containers](../../glossary/container.md) 共用這台 VM 的 guest kernel。每個 [pod](../../glossary/pod.md) 各有一台 VM，和每個 container 各有一台 VM 並不相同。同一個 host 上的 VM 即使各自執行自己的 guest kernel，仍可共用實體硬體。請參閱架構概覽中的[哪些 workload 共用 guest kernel](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)。

## 何時適用？ {#when-to-use-it}

當 agent 需要完整的 Linux [workspace](../../glossary/workspace.md)，而且 workload 需要自己的 kernel 時，就選用這種邊界。例如，可以執行原生建置流程和測試套件，而不讓這些 process 直接在 host kernel 上執行。

## 這個邊界不涵蓋什麼？ {#what-the-boundary-does-not-cover}

Guest 可以使用 host 選擇開放的檔案。如果共用專案目錄可寫入，guest 就能修改其中的 host 檔案。請確認 guest 能透過儲存空間和網路存取哪些資源。如果要重複使用 [snapshot](../../glossary/snapshot.md)，請在分享前確認它包含磁碟資料、記憶體內容，還是兩者都有。

如需了解有哪些 VMM，以及哪些 sandbox 產品使用這些 VMM，請參閱[架構概覽](../../agent-sandbox-architectures.md#hardware-backed-linux-environments)。
