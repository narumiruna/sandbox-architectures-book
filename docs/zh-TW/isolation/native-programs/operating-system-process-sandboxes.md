# 作業系統層級的 process sandbox {#operating-system-process-sandboxes}

[Operating-system process sandbox](../../glossary/operating-system-process-sandbox.md) 讓 [agent](../../glossary/agent.md) 能在 [host](../../glossary/host.md) 上使用原生指令，同時限制這些指令能存取的資源。Sandbox 內沒有獨立的作業系統。

## 誰處理請求？ {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md) 的測試執行程式要求開啟 `total.c` 時，它的 [process](../../glossary/process.md) 會向 host [kernel](../../glossary/kernel.md) 發出 [system call](../../glossary/system-call.md)，由 host kernel 處理。在 Linux 上，[mount namespace](../../glossary/namespace.md) 可以讓 process 看見專案，卻看不到 host 的私有目錄。[Seccomp](../../glossary/seccomp.md) 過濾器可以阻擋特定類型的 system call，但無法單獨強制執行個別檔案路徑的規則。

例如，[Anthropic Sandbox Runtime 的 `0bbebed0` 修訂版本](https://github.com/anthropic-experimental/sandbox-runtime/blob/0bbebed0aa9a8e628dc4df8bc30293550a1988eb/README.md) 在 Linux 上使用 [Bubblewrap](https://github.com/containers/bubblewrap)，在 macOS 上使用 Seatbelt 設定檔。它也透過網路代理檢查目的地是否在允許範圍內。不同 host 平台使用的機制不同；請在實際執行 agent 的平台上驗證行為。

## 哪些資源仍會共用？ {#what-stays-shared}

Sandbox 內外的 process 使用同一個 host kernel。Kernel 可以讓各個 sandbox 看見不同的檔案，但如果 host 目錄透過可寫入的 [mount](../../glossary/mount.md) 開放，程式仍可修改其中的檔案。

## 何時適用？ {#when-to-use-it}

如果在本機執行的 agent 需要使用目前作業系統的原生工具，但不應繼承不受限制的 host 存取權，就選用這種邊界。這適合使用開發者既有命令列工具的測試執行程式。

## 這個邊界不涵蓋什麼？ {#what-the-boundary-does-not-cover}

隱藏檔案不會移除已交給 process 的 [credentials](../../glossary/credential.md)，檔案規則也不會限制網路存取。請檢查繼承的環境變數和已開啟的連線。請使用無害的檔案來[驗證存取規則](../../practice/verification/verifying-access-rules.md)，並另外檢查網路存取。接著用子 process（例如由套件管理員啟動的測試執行程式）再做一次檔案檢查。
