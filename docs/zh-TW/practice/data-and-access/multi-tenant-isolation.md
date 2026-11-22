# 多 tenant 隔離 {#multi-tenant-isolation}

把執行中的作業分開，並檢查作業結束後保留的資料可由誰存取。在 [Lamp 操作範例](../design/from-issue-to-patch.md)中，Lamp 和 Cedar 是兩個 [tenants](../../glossary/tenant.md)：兩個必須分開處理工作和資料的群組。即使 Cedar 知道 ID 和檔名，也不能讀取 Lamp 的 issue、workspace 或送審輸出。

## 決定哪些作業共用邊界 {#decide-what-shares-a-boundary}

[Isolation unit](../../glossary/isolation-unit.md) 是一組 [workloads](../../glossary/workload.md)，它們共用同一個 [isolation boundary](../../glossary/isolation-boundary.md) 實例。決定哪些 workloads 共用同一個實例，與選擇隔離機制是兩回事。[架構概覽](../../agent-sandbox-architectures.md#which-workloads-share-a-guest-kernel)比較不同的系統，說明即使都採用 [virtual machines (VMs)](../../glossary/virtual-machine.md)，也可以用不同方式將作業分組。

| 各自擁有一個邊界的對象 | 好處 | 哪些狀態可能延續 |
| --- | --- | --- |
| 每個請求 | 每項作業都能從乾淨的環境開始。 | 如果換掉邊界實例，邊界內不會留下上一項作業的任何資料或狀態；外部儲存服務仍須檢查。每項作業都要重新設定。 |
| 每個 session | 多個步驟可以重複使用同一個編輯器、workspace 或建置輸出。 | 檔案和 process 會在同一個 session 的各次請求間保留。只有獲授權存取該 session 的呼叫者才能重新連接。 |
| 每個 tenant | 同一個 tenant 的作業可以使用一個長期運作的環境。 | 若無額外邊界，該 tenant 的作業和使用者會共用一個 runtime。只有在這些作業可以共用該狀態時才適用。 |

## 只共用明確允許的資源 {#keep-shared-resources-deliberate}

Lamp 每次嘗試建置時都會啟動一台全新的 VM，即使是同一個 tenant 重試也一樣。[Control plane](../../glossary/control-plane.md) 根據請求者驗證過的身分，將 tenant 和該次執行綁定到 VM。Workspace 服務先檢查這個綁定關係，再將該次執行用完即丟的 [workspace](../../glossary/workspace.md) 掛載在 `/work`。像 `lamp/work` 這樣的名稱只是標籤，不能取代權限檢查。

作業可以共用乾淨的唯讀編譯器映像檔，但不共用 workspace 磁碟、執行中的 VM 或可寫入的快取（保留輸入或建置結果供日後使用的儲存空間）。本範例在掛載作業資料後不會儲存任何 snapshot。如果後續設計需要私有快取，快取服務必須先檢查 tenant 的存取權，再傳回項目。

Issue 處理元件在每次呼叫時檢查 tenant、操作和紀錄。審查儲存服務在每次讀取時檢查 tenant，以及該次執行所指派的審查者。光是 Lamp 的成員還不夠。診斷紀錄也會按 tenant 限制範圍，供處理該次執行的維運人員使用。獨立的 VM 無法阻止這些儲存服務把資料交給錯誤的 tenant。

## 用測試資料檢查 {#check-with-dummy-data}

提供 Lamp 和 Cedar 測試用的 workspace 和 artifact，使用相同檔名，但在檔案中放入不同的辨識文字。確認各 tenant 能讀取自己的辨識文字，卻無法掛載對方的 workspace 或取得對方的 artifact。確認只有獲授權的 Lamp 呼叫者可以讀取 `LAMP-17`。如果有私有快取，就在每個 tenant 的同名項目中放入不同的辨識文字，確認各自取得自己的值。在曾執行 Lamp 作業的基礎設施上啟動一項全新的 Cedar 作業，確認找不到 Lamp 的辨識文字。請參閱[驗證存取規則](../verification/verifying-access-rules.md)中的本機範例；這些檢查不涵蓋共用 host 的所有影響。

下一篇：[Control plane](../operations/control-planes.md)說明服務如何啟動 worker、掛載正確 tenant 的 workspace，並確認清理完成。
