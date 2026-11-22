# Control plane

Control plane 是系統中管理執行環境的部分。它決定 [sandbox](sandbox.md) 在哪裡執行、何時啟動或停止等事項。它可以選擇並設定限制程式碼的機制，但本身不是那個機制。

## 範例

建置服務收到測試 Lamp 的請求。它的 control plane 依照核准的設定啟動一部 [virtual machine (VM)](virtual-machine.md)，將 Lamp 的 [workspace](workspace.md) 交給它，並在執行結束時移除它。測試期間，開啟 `total.c` 的請求由 VM 的 [guest kernel](guest.md) 處理，而不是由 control plane 處理。

## 管理與執行的差異

Control plane 可以選擇執行用的 [runtime](runtime.md)、要求特定的 workspace，並追蹤環境是否就緒。例如，[Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/README.md) 在 Kubernetes 上提供管理 API，用來定義和申領 sandbox。[Isolation boundary](isolation-boundary.md) 由 runtime 提供，因此同類型的管理請求不代表會有同樣的隔離方式。

## 何時需要留意

當許多工作都需要 sandbox 時，使用 control plane 分配環境，並在工作完成後清理。服務必須以 [authorization](authorization.md) 決定誰可以建立或申領環境，以及可以掛接誰的檔案。如果 control plane 把錯誤的 [tenant](tenant.md) 的 workspace 分配給 sandbox，execution boundary 無法補救。請參閱[分開處理封裝、管理與隔離](../sandbox-isolation-boundaries.md#keep-packaging-management-and-isolation-separate)。

[返回詞彙表](index.md)
