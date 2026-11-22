# 可觀測性與除錯 {#observability-and-debugging}

從最後一個成功的步驟查起。Worker 一直沒有就緒、操作遭存取規則阻擋，以及編譯器執行後回報錯誤，需要用不同的方法處理。[Observability](../../glossary/observability.md) 是指有足夠的證據分辨這些情況。光看 `failed` 這類單一狀態並不夠。

用 [Lamp 範例](../design/from-issue-to-patch.md)追蹤一次執行，依序查看查詢議題、設定 worker、建置和清理的過程。

## 找出證據對應的層級 {#match-the-evidence-to-the-layer}

[Control plane](../../glossary/control-plane.md) 記錄收到執行請求、執行就緒和停止的時間，並另外記錄清理狀態。[Runtime](../../glossary/runtime.md) 回報指令結果及觸及執行上限的事件。工具處理程式記錄議題存取是否獲准；收集器記錄匯出是否成功。用不含機密的請求 ID 和嘗試 ID 串起這些紀錄。用 UTC 時間戳記建立時間軸，並用不會突然跳動的時鐘記錄各段耗時。

以下是三次彼此獨立的虛構嘗試。時間戳記和紀錄摘錄只用來示範如何判讀證據。

| 嘗試與狀態（UTC） | 遮蔽敏感資訊後的證據 | 負責層級與下一步檢查 |
| --- | --- | --- |
| A1：`10:00:00 provisioning` → `10:00:30 timed_out` | `workspace_attach_timeout`；沒有 `ready` 事件。 | Control plane 和工作區服務：查明為何無法掛接已核准的副本。確認尚未配置完成的資源已清理。 |
| A2：`10:01:00 lookup` → `10:01:01 access_denied` | 議題處理程式在讀取任何紀錄前，就拒絕了超出 Lamp 範圍的模擬請求。 | 議題處理程式的負責人：確認這次執行的範圍。不要為了讓檢查通過而放寬規則。 |
| A3：`10:02:00 ready` → `10:02:02 build_failed` | `compile_failed`；結束狀態碼為 `1`。測試未執行。 | 請求者可以用已核准的副本重現建置過程，找出錯誤原因。不保留修補檔草稿或編譯器的原始紀錄。 |

操作遭拒是一個事件，不一定是 session 的最終結果。要把後續失敗歸因於該項拒絕前，先確認接著執行了哪道指令。如果懷疑碰到 [resource limit](resource-limits.md)，請查看強制執行限制的層級是否明確回報觸及上限的事件，不要只靠結束狀態碼猜測。

## 保護診斷紀錄 {#keep-diagnostic-records-safe}

只保留可安全留存的中繼資料：執行 ID、嘗試 ID、時間戳記、階段、狀態和原因代碼。不要記錄環境傾印、原始引數、議題文字、[credential](../../glossary/credential.md) 的值或工作區內容。只有指派給該 tenant 的維運人員可以存取這些紀錄。服務維運人員會保留清理紀錄，直到確認移除完成，再於 30 天後讓該次嘗試的診斷紀錄到期。`cleaned_up` 事件只確認 worker 已清理，不表示已接收供審查的檔案或診斷紀錄已刪除。

回到[決策紀錄](../design/from-issue-to-patch.md#fill-in-your-decision-record)，為每個副本指定負責人和到期時間。接著依照[驗證存取規則](../verification/verifying-access-rules.md)，測試獲准的操作是否成功，以及禁止的操作是否因預期的原因而失敗。
