# MicroVM

[MicroVM](../../glossary/microvm.md) 是一種 [virtual machine (VM)](../../glossary/virtual-machine.md)，設計目標是比通用 VM 更輕量，減少啟動和執行所需的資源。它通常提供較少的虛擬裝置，但仍會執行自己的作業系統 [kernel](../../glossary/kernel.md)。如果工作需要獨立的 kernel，且提供的虛擬裝置能滿足需求，可以選用 microVM。光看名稱裡的「micro」，無法判斷工作會多快開始或會用多少記憶體。

## 開啟檔案的請求送到哪裡？ {#where-the-file-request-goes}

1. [Lamp](../../practice/design/from-issue-to-patch.md) 的測試執行程式要求開啟 `total.c`。這個 [system call](../../glossary/system-call.md) 由 Linux [guest kernel](../../glossary/guest.md) 處理，而不是由 [host](../../glossary/host.md) kernel 處理。
2. Guest kernel 在自己的檔案系統中查找這個路徑。如果檔案位於虛擬磁碟上，guest kernel 會視需要讀取該裝置。
3. 在 [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#host-integration) 中，虛擬磁碟可以用 host 上的一個檔案當作儲存空間。Guest 透過這個裝置看到的是虛擬磁碟，而不是 host 的檔案系統。

Firecracker 是 [virtual machine monitor (VMM)](../../glossary/virtual-machine-monitor.md)，負責提供虛擬裝置，並[使用 KVM 執行 guest 的虛擬 CPU](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#internal-architecture)。它的[裝置模型](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#machine-model)提供虛擬儲存和網路裝置，但不提供圖形顯示裝置。請確認所選 VMM 提供哪些裝置，不要假設所有 microVM 都提供相同的裝置。

## 決定要共用和保留什麼 {#decide-what-to-share-and-keep}

- **Kernel：** 同一台 microVM 裡的 process 共用該 VM 的 guest kernel。如果不同工作不能共用 kernel，就為每項工作各分配一台 microVM，不要把多項工作放進同一台。
- **狀態：** 如果同時支援 [cold boot](../../glossary/cold-boot.md) 和從 [snapshot](../../glossary/snapshot.md) 還原，請比較兩種方式。例如，[Firecracker v1.11.0 的 snapshot](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/snapshotting/snapshot-support.md#overview) 會保留 guest 的記憶體內容和模擬硬體的狀態；虛擬磁碟的底層儲存空間則由維運人員另外管理。重複使用前，請檢查 snapshot 和磁碟是否留有工作資料。
- **存取：** 使用獨立的 kernel，並不會阻止 guest 存取可寫入的共用目錄，也不會阻擋對外的網路流量。請設定並[驗證存取規則](../../practice/verification/verifying-access-rules.md)，確認工作可以存取哪些檔案、網路目的地和 credentials。

如果工作不需要自己的 Linux kernel，請參閱 [MicroVM vs gVisor](microvm-vs-gvisor.md)。
