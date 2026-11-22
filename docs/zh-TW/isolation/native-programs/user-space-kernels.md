# User-space kernel {#user-space-kernels}

[User-space kernel](../../glossary/user-space-kernel.md) 讓 [agent](../../glossary/agent.md) 不必啟動獨立的 Linux [guest](../../glossary/guest.md)，也能執行 Linux 程式。它實作這些程式所需的 Linux 介面，因此程式的請求不會直接送到 [host](../../glossary/host.md) [kernel](../../glossary/kernel.md)。

## 誰處理請求？ {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md) 的測試執行程式在 [gVisor](https://gvisor.dev/docs/architecture_guide/intro/) 內透過 [system call](../../glossary/system-call.md) 要求開啟 `total.c` 時，由 gVisor 的 **Sentry** 處理。Sentry 會在測試執行程式可見的檔案系統中解析該路徑。gVisor 可以自行向 host 發出有限的請求來取得資料，而不是原封不動地轉送 workload 的 system call。

## 哪些資源仍會共用？ {#what-stays-shared}

同一個 gVisor sandbox 裡的程式共用 Sentry。gVisor 的底層資源仍由 host kernel 提供。相較之下，[VM](../../glossary/virtual-machine.md) 會啟動 guest kernel。在 [process sandbox](operating-system-process-sandboxes.md) 中，程式則會自行向 host kernel 發出 system call。

## 何時適用？ {#when-to-use-it}

如果需要執行 Linux [containers](../../glossary/container.md)，但想在 workload 和 host kernel 之間加一層隔離，就選用這種邊界。由於 gVisor 重新實作了 Linux 介面，程式所依賴的行為可能[不受 gVisor 支援，或在其中有不同的運作方式](https://gvisor.dev/docs/user_guide/compatibility/)。請實際驗證安裝、建置和測試步驟，而不只是確認指令能啟動。

## 這個邊界不涵蓋什麼？ {#what-the-boundary-does-not-cover}

Sentry 依照接收到的檔案系統檢視提供存取。它不負責決定 agent 應該能讀取哪些 Lamp 資料。請確認 [runtime](../../glossary/runtime.md) 只開放預期的 [workspace](../../glossary/workspace.md) 和網路存取。
