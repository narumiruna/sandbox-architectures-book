# gVisor

[gVisor](https://gvisor.dev/docs/architecture_guide/intro/) 不必啟動獨立的 Linux [guest kernel](../../glossary/guest.md)，就能執行 Linux [container](../../glossary/container.md)。它的 [user-space kernel](../../glossary/user-space-kernel.md) 稱為 **Sentry**，負責處理 sandbox 內程式發出的請求。取捨在於相容性：gVisor 自行實作 Linux 介面，因此有些功能不受支援，有些功能的行為則不一樣。

## 開啟檔案的請求送到哪裡？ {#where-the-file-request-goes}

1. [Lamp](../../practice/design/from-issue-to-patch.md) 的測試執行程式透過 [system call](../../glossary/system-call.md) 要求開啟 `total.c`。Sentry 會根據 sandbox 看得到的檔案系統來處理，不會把 workload 的 system call 直接轉送給 [host](../../glossary/host.md) kernel。
2. 如果設定為開放 host 上的檔案，gVisor 可以透過名為 **Gofer** 的輔助 process [提供這些掛載點的存取](https://gvisor.dev/docs/user_guide/filesystem/)。依設定而定，Gofer 可以讓 Sentry 直接操作已開放的檔案，不必每次都由 Gofer 處理。gVisor 的底層資源仍由 host kernel 提供。隱藏 host 上的其他檔案，並不會隱藏刻意掛載到 sandbox 裡的檔案。

## 更換 platform 會改變什麼？ {#what-changes-with-the-platform}

gVisor 的 [platform](https://gvisor.dev/docs/architecture_guide/platforms/) 是讓 Sentry 攔截 system call 並管理程式執行的機制。**systrap** 不需要 CPU 支援虛擬化。**KVM** platform 使用[硬體輔助虛擬化](hardware-backed-virtual-machines.md)，但仍由 Sentry 提供 Linux 介面。使用 KVM 並不會讓 gVisor 變成會啟動自己 Linux kernel 的 [MicroVM](microvm.md)。

## 選用 gVisor 前要確認什麼？ {#what-to-verify-before-choosing-gvisor}

- **Runtime：** gVisor 提供的 `runsc` 是一種 [OCI](../../glossary/open-container-initiative.md) [container runtime](../../glossary/container-runtime.md)。請確認部署設定會用它來執行這項工作；光是選用某個 container 映像檔，並不會決定隔離邊界。
- **相容性：** 請查閱[支援的 Linux 功能](https://gvisor.dev/docs/user_guide/compatibility/)。例如，gVisor 不支援從 sandbox 內掛載原生區塊裝置。請實際執行完整的工作，包括設定環境和測試。Shell 能啟動，不代表能完成建置。
- **共用：** 同一個 gVisor sandbox 裡的程式共用 Sentry。請先決定哪些工作可以共用同一個 sandbox，再針對掛載項目、網路存取和 credentials [驗證存取規則](../../practice/verification/verifying-access-rules.md)。

如需選擇指引，請參閱 [MicroVM vs gVisor](microvm-vs-gvisor.md)。
