# Workspace 與 artifact {#workspaces-and-artifacts}

讓 worker 修改專案的副本，只交回審查者需要的檔案。在 [Lamp 操作範例](../design/from-issue-to-patch.md)中，Linux worker 在 `/work` 建置並測試修正。它可以交回純文字修補檔與測試輸出供審查，但不能發布修正。

## 決定 worker 可以修改哪些檔案 {#choose-what-the-worker-can-change}

[Workspace](../../glossary/workspace.md) 是一項作業可以使用的一組檔案。[Mount](../../glossary/mount.md)（掛載）讓檔案可透過某個路徑存取，不一定會複製檔案。Checkout 是從儲存庫取出的指定版本原始碼目錄樹。

| Workspace 的配置方式 | 對原始 checkout 的影響 | 適用情況 |
| --- | --- | --- |
| 唯讀 mount | Worker 可以讀取檔案，但無法透過這個 mount 修改檔案。修改必須寫到另一個可寫入的位置。其他 process 仍可能變更原始檔案。 | 檢查檔案，或將所有建置輸出寫到其他位置。 |
| 可寫入的共用目錄 | 如果該目錄就是原始 checkout，編輯、刪除和未完成的寫入都會立即改動原始 checkout，即使作業失敗也一樣。 | 可信任且刻意要直接修改原始檔案的本機工作流程。 |
| 用完即丟的副本，僅明確匯出指定檔案 | Worker 只修改自己的副本。原始 checkout 不會掛載，worker 也沒有其他途徑可寫入原始 checkout。除非獨立的收集元件接受輸出，否則不會交回任何資料。 | 必須修改原始碼，但不能在審查前套用變更的建置。 |

唯讀不等於保密：worker 仍可讀取 mount 開放的所有內容。不論採用哪種方式，都只提供必要的輸入。不要包含本機設定或 [credentials](../../glossary/credential.md)。

## 決定哪些檔案可以離開 `/work` {#decide-what-leaves-work}

[Artifacts](../../glossary/artifact.md) 是作業結束後特別挑出來保留的輸出。Lamp 的審查者只需要兩個檔案：`change.patch`（上限 128 KiB）和 `test.log`（上限 64 KiB）。這些上限是範例中對接收檔案的限制，與 worker 的磁碟容量上限分開計算。

1. Workspace 服務依照 [control plane](../../glossary/control-plane.md) 的執行指派作業。它將核准版本的原始碼、測試及工作摘要複製到一個新的 [guest](../../glossary/guest.md) 磁碟上，該磁碟掛載於 `/work`。它不複製儲存庫歷史紀錄、設定或機密資料，也不掛載原始 checkout。Worker 可以修改副本，包括其中的測試。
2. 建置與測試指令回報成功且 worker 停止後，位於 worker 的 [isolation boundary](../../glossary/isolation-boundary.md) 之外的收集元件，只會從該次執行的磁碟讀取指定的兩個檔案。只有在兩者皆為符合大小限制的一般 UTF-8 文字檔時，才會一併接受，且不會跟隨檔案系統連結。如果檔案缺少、過大或無效，收集元件會拒絕結果，不會公開部分輸出。它採用 control plane 提供的執行 ID、基準版本及該次嘗試的狀態，而不信任 worker 提供的標籤。
3. 審查儲存服務僅接受收集元件上傳，且只允許該次執行指定的 Lamp 審查者讀取。提出請求不會自動取得審查存取權。服務以不受信任的文字呈現這兩個檔案，絕不把它們當成指令或套用修補的許可。服務在接收後七天刪除這兩份檔案。本範例不會在備份中另外保留副本。
4. 即使匯出失敗，workspace 服務也會捨棄 `/work`，包括修改後的原始碼、二進位檔和暫存檔。[Control plane 會確認清理完成](../operations/sandbox-lifecycle.md#what-gets-deleted-and-when)；審查儲存服務的到期刪除則另外處理。

檢查檔名及大小，不等於檢查文字內容。Worker 可以將它能讀取的任何資料寫入這兩個檔案中的任一個。一開始就不要把機密或無關的資料放進 workspace。

下一篇：[網路 policy](network-policy.md)說明為什麼 worker 不必存取網路服務就能交換這些檔案。
