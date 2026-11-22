# 部署模式 {#deployment-patterns}

決定 worker 要在哪裡執行、由誰維運時，要把這些問題與 [sandbox 隔離哪些東西](choosing-a-sandbox.md) 分開考量。在遠端基礎設施上執行的 worker，可以自行代管，也可以交由服務供應商管理。在這四種配置中，都是由同一個唯讀 [tool](../../glossary/tool.md) 取得 Lamp 的 issue `LAMP-17`，再由獨立的 Linux worker 修正一個小型 C 程式算錯總數的問題。Worker 在副本中編譯和測試，再傳回文字修補檔和測試輸出供審查。它不能發布修正。

## 哪些做法不變 {#what-stays-the-same}

Linux worker 取得的是用完即丟的 [workspace](../../glossary/workspace.md)，而不是把原始 repository 以可寫入的方式 [mount](../../glossary/mount.md) 進來。Issue tool 讀取的是虛構的測試資料，不使用任何服務 [credentials](../../glossary/credential.md)。如果需要讀取 issue 的 credentials，由下文列出的負責人保管，不會交給指令碼或 worker。任何發布權限都屬於此工作流程之外的獨立角色。將修補檔和記錄保留為 [artifacts](../../glossary/artifact.md)，僅允許審查人員存取，並設定明確的到期時間。

## 各種配置由誰維運？ {#who-operates-each-layout}

### 本機工作站 {#local-workstation}

開發者維運指令碼和 Linux 的 runtime，並負責 issue tool 和任何讀取用的 credentials。本機控制器建立暫存副本、停止 worker，並在執行結束後移除副本。開發者限制審查目錄的存取，並在審查期限結束時刪除已儲存的輸出。這種配置讓整個工作流程留在開發者的電腦上，但 runtime 仍須阻止 worker 存取開發者的家目錄和原始簽出目錄。

### 持續整合（CI） {#continuous-integration-ci}

[Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration)（CI，持續整合）可以自動啟動工作，但 CI 不是隔離機制。在這種配置中，runner 的維運人員負責維護兩個 [runtimes](../../glossary/runtime.md)。專案團隊選擇原始碼的修訂版本，負責 issue tool 和任何讀取用的 credentials，並決定誰可以讀取 artifacts，以及可以讀取多久。CI 工作控制器準備暫存副本，並在工作結束後刪除，即使工作失敗也一樣。CI 的 artifact 儲存空間會依照專案設定的時程讓已儲存的輸出到期。工作可以使用專案既有的審查流程，而不必繼承該流程的發布權限。

### 自行代管的服務 {#self-hosted-service}

內部平台團隊維運兩個 runtime，並在自己維運的基礎設施上為每次執行提供暫存空間，不論設施位於組織內部或雲端。各專案團隊負責自己的原始碼、issue tool 及其讀取權限，以及審查存取的 [policy](../../glossary/policy.md)。平台團隊的 [control plane](../../glossary/control-plane.md) 會停止執行失敗或已到期的 worker、移除暫存空間，並依照專案 policy 讓保留的輸出到期。平台團隊也必須為 runtime 套用修補、監控容量並處理故障。

### 代管 worker 服務 {#managed-worker-service}

客戶維運指令碼的 runtime，並負責 issue tool 和任何讀取用的 credentials。服務供應商維運 Linux runtime，並建立及移除 worker 的暫存空間。客戶選擇要使用的原始碼副本，並在自己的審查儲存空間中管理存取和到期時間。客戶也必須確認供應商會移除或保留哪些資料，包括工作取消後的情況。結束工作不一定會刪除另外儲存的副本，例如記錄、快取或 [snapshots](../../glossary/snapshot.md)。

## 分別做三項決定 {#make-three-separate-decisions}

1. **執行位置：** 核准的檔案可以離開工作站或組織嗎？記錄工作在哪裡執行，以及狀態和輸出儲存在哪裡。
2. **權責：** 由誰為 runtime 套用修補、處理失敗的工作、驗證清理結果，以及支付容量費用？比較自行代管服務所需的人力時間和基礎設施成本，以及使用代管服務時供應商收取的費用和客戶仍須負責的工作。
3. **執行邊界：** 本機 worker 可以使用 [virtual machine (VM)](../../glossary/virtual-machine.md)；遠端 worker 也可能共用 [host](../../glossary/host.md) 的 [kernel](../../glossary/kernel.md)。確認由哪個 runtime 強制執行 [isolation boundary](../../glossary/isolation-boundary.md)、哪些工作共用這道邊界，以及哪些東西可以跨越它。實作範例請參閱[架構概覽](../../agent-sandbox-architectures.md)。

下一步：先從 [Tool 的授權](tool-authorization.md) 開始設定存取規則，了解即使指令碼在 sandbox 內執行，查詢 issue 的 tool 仍必須檢查哪些項目。
