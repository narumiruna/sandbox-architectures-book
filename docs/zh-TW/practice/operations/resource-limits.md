# 資源上限 {#resource-limits}

[Resource limits](../../glossary/resource-limit.md) 決定 worker 能用多少資源。存取規則決定 worker 能接觸哪些資源。磁碟上限可以防止建置作業用光儲存空間，但只有存取規則能防止 worker 存取其他專案的檔案。

在 [Lamp 範例](../design/from-issue-to-patch.md)中，worker 的資源額度必須足以編譯和測試 C 程式，也要足以寫入建置檔案。

## 設定資源額度，決定達到上限時如何處理 {#set-a-budget-and-decide-what-happens-at-the-limit}

以下上限僅供示範，不是預設值，也不是實測得出的需求。計算用量時，要把整個 worker 算進去，包括編譯器和測試 process，而不只算第一道指令。[Control plane](../../glossary/control-plane.md) 負責選定額度、決定是否受理工作，並強制執行時限。[Runtime](../../glossary/runtime.md) 限制執行時的資源用量，工作區服務則限制暫存空間。

| 限制項目 | 額度範例 | 達到上限時如何處理 |
| --- | --- | --- |
| CPU | 每個計量區間內，最多可用相當於一顆 CPU 的執行時間。 | Runtime 會讓 worker 降速，而不是停止它。這項上限不會為 Lamp 保留一顆 CPU。 |
| 記憶體 | 256 MiB 的 VM 記憶體，由 Linux 和 worker 的所有 process 共用。 | 如果 runtime 回報因記憶體上限而失敗，就停止執行。不要在條件不變的情況下重試。 |
| 磁碟 | 整個可寫入的 `/work` 磁碟有 64 MiB，包括事先備妥的輸入與暫存的建置檔案。 | 超出額度的寫入會失敗。如果磁碟上限導致建置失敗，就傳回可安全揭露的原因代碼，並丟棄不完整的檔案。 |
| 時間 | 排隊等待、啟動 worker 和執行指令各有 30 秒，分開計時。 | 到達時限時，讓排隊中的請求失效，或停止已經開始的嘗試。記錄是哪個階段逾時。 |
| 容量 | 每個 [tenant](../../glossary/tenant.md) 只能占用一個已配置的 worker 名額，包括配置和清理期間；另可有最多兩個請求等待。 | 只有佇列還有空位時，才讓請求排隊。拒絕超額的請求；只要第一個 Lamp worker 還占著名額，就不能啟動第二個。 |

## 不要把不完整的輸出當成成功 {#do-not-mistake-partial-output-for-success}

如果 Lamp 在連結時碰到磁碟上限，可能會留下不完整的二進位檔，測試甚至可能還沒開始。嘗試失敗、取消或逾時時，請傳回狀態和可安全揭露的原因代碼，不要傳回不完整的修補檔、原始紀錄或二進位檔。只有在強制執行限制的層級回報時，才記錄是哪項上限造成失敗。Control plane 會停止 worker，並依照與成功時相同的[清理規則](sandbox-lifecycle.md#what-gets-deleted-and-when)處理。經授權的請求者可以在解決問題後重新嘗試；若沿用相同額度自動重試，可能會再次失敗。

收集器另外強制執行[輸出大小上限](../data-and-access/workspaces-and-artifacts.md#decide-what-leaves-work)。即使建置成功且測試通過，匯出仍可能失敗。這種情況也不要只發布成對輸出中的一部分。

接下來：[可觀測性與除錯](observability-and-debugging.md)說明如何分辨觸及上限、存取遭拒和建置失敗。
