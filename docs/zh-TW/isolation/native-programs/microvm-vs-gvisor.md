# MicroVM vs gVisor

先問一個問題：**這項工作需要自己的 Linux kernel 嗎？** 如果需要，先找一種 guest kernel 和裝置都符合需求的 [MicroVM](microvm.md)。如果不需要，而且 Linux [container](../../glossary/container.md) 能在 [gVisor](gvisor.md) 上正常執行，就可以把 gVisor 列入考量。MicroVM 是一種 [virtual machine](../../glossary/virtual-machine.md)，gVisor 則是 [user-space kernel](../../glossary/user-space-kernel.md) 的一種實作。光看名稱，無法判斷哪個方案在你的部署環境中更安全或更快。

## 比較執行邊界 {#compare-the-execution-boundaries}

當程式要求開啟檔案時，關鍵差異在於[由哪個元件處理請求](../../sandbox-isolation-boundaries.md#sandboxes-for-operating-system-workloads)。只要設定得當，兩種邊界都能開放相同的專案檔案。

| 要確認的事項 | MicroVM | gVisor |
| --- | --- | --- |
| 誰處理 Linux [system call](../../glossary/system-call.md)？ | 在 VM 內執行的 Linux [guest kernel](../../glossary/guest.md)。 | [Sentry](https://gvisor.dev/docs/architecture_guide/intro/#how-does-gvisor-provide-isolation)，即使使用 KVM platform 也是如此。 |
| [Host](../../glossary/host.md) 必須提供什麼？ | 使用硬體輔助虛擬化的 microVM 需要支援的虛擬化後端。例如，[Firecracker v1.11.0 使用 KVM](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/design.md#internal-architecture)。 | 需要受支援的 Linux host。[systrap 不需要硬體輔助虛擬化](https://gvisor.dev/docs/architecture_guide/intro/#how-does-gvisor-provide-isolation)，但 [KVM platform 會用到](https://gvisor.dev/docs/architecture_guide/platforms/#kvm)。 |
| 工作可以使用哪些介面和資源？ | 所選 guest kernel 的介面，以及 VM 開放的裝置。 | [gVisor 實作的 Linux 介面](https://gvisor.dev/docs/user_guide/compatibility/)，以及 runtime 開放的資源。 |
| 哪些工作共用一道邊界？ | 分配到同一台 microVM 的工作共用該 VM 的 guest kernel。 | 分配到同一個 gVisor sandbox 的工作共用該 sandbox 的 Sentry。 |

## 用一項實際工作來選擇 {#make-the-choice-with-one-real-job}

1. **確認不可少的需求。** 如果測試要驗證某個特定 Linux kernel 建置版本的行為，就使用能啟動該版本的 microVM。如果工作只是在以 container 映像檔建立的環境中編譯和測試 user-space 程式，也可以試用 gVisor。只通過基本的 smoke test 還不夠，請實際執行安裝、建置和測試。
2. **在兩種環境驗證相同的存取規則。** 使用相同的專案修訂版本，並只開放每項工作應有權使用的檔案、網路目的地和 credentials。確認哪些工作會共用同一個 sandbox，以及哪些資料或狀態會留到下次執行。這些都要另外決定，不能只看上表的隔離機制。
3. **只測量符合需求的候選方案。** 記錄 runtime 版本、platform，以及是從頭啟動、從保存的狀態還原，還是領用已備妥的 sandbox。[測量](../../practice/verification/measuring-a-sandbox.md)預期並行程度下的三項數值：到能執行第一個指令所需的時間、完成工作所需的時間，以及 host 的記憶體用量。不要拿一方從頭啟動的結果和另一方使用已備妥 worker 的結果相比，卻把差異全歸因於隔離方式。

如需了解同時提供這兩種選項的現有系統，請參閱 [Agent Substrate 的架構](../../agent-substrate.md)。
