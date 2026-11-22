# Control plane {#control-planes}

[Control plane](../../glossary/control-plane.md) 決定 [sandbox](../../glossary/sandbox.md) 在哪裡執行、會收到什麼，以及何時移除。[Runtime](../../glossary/runtime.md) 負責準備執行環境，並在 [isolation boundary](../../glossary/isolation-boundary.md) 內執行程式碼。如果 control plane 把專案檔案掛載到錯誤的執行環境，即使隔離邊界再嚴密，也無法保護專案。

在 [Lamp 範例](../design/from-issue-to-patch.md)中，control plane 準備一個獨立的 Linux worker，在原始碼副本上執行建置與測試，再移除 worker 及其副本。

## 從收到請求到完成清理 {#from-request-to-cleanup}

1. **檢查授權並選擇 policy。** Control plane 檢查請求者是否可以為 `LAMP-17` 啟動 Lamp [session](../../glossary/sandbox-session.md)，並使用指定的原始碼版本。它會把這些輸入綁定到該次執行。Control plane 的 [policy](../../glossary/policy.md) 訂出 runtime、workspace 服務與收集元件必須遵守的要求，再由這些元件執行。Issue tool 仍須自行檢查紀錄的存取權。
2. **選擇 host 並準備 worker。** Control plane 選擇一台 [host](../../glossary/host.md)，這台 host 必須有足夠的資源，並支援啟動全新的 [virtual machine (VM)](../../glossary/virtual-machine.md)。它向 workspace 服務要求核准的 Lamp 副本，並向 runtime 要求一台 VM。在允許執行第一道指令前，它會檢查回報的設定：workspace 正確、映像檔乾淨、資源限制已設定，且沒有對外網路連線。如果有任何要求無法達成，請在佇列等待期限內繼續等待，或將該次嘗試判定為失敗。不要改用防護較弱的配置。
3. **執行、停止並收集。** VM 限制執行中的程式碼只能使用開放的資源。Runtime 回報指令狀態，control plane 則停止 worker。只有在建置與測試皆完成並通過之後，收集元件才可以接收指定的兩個文字檔。審查儲存服務會另外檢查審查者的存取權。
4. **確認清理完成。** 不論以何種方式結束，即使設定只完成一部分或匯出失敗，control plane 都會追蹤資源是否已移除。如果無法確認資源已移除，就不要再使用這些資源，並重試清理及通知維運人員。審查儲存服務負責讓接收的 [artifacts](../../glossary/artifact.md) 到期；清理 worker 不會讓這些檔案到期。

## 誰負責什麼？ {#who-owns-what}

| 元件 | 在此範例中的責任 |
| --- | --- |
| Control plane | 將每次執行綁定到對應的 [tenant](../../glossary/tenant.md)、issue 與版本；選擇配置，並追蹤就緒狀態、期限和清理進度。 |
| 直譯器與 VM runtime | 直譯器限制指令碼可以呼叫哪些操作。VM runtime 只開放設定的資源，並回報 worker 的狀態與移除結果。 |
| Issue tool 處理元件 | 檢查對 `LAMP-17` 的存取權，並只傳回獲准存取的欄位。 |
| Workspace 服務 | 將核准的 Lamp 副本放到該次執行使用的磁碟上、強制執行磁碟容量上限，並確認磁碟已移除。 |
| 收集元件 | 驗證該次執行磁碟上的兩個檔案，並寫入對應的審查項目。 |
| 審查儲存服務 | 對審查者的每次讀取檢查授權，並在期限屆滿時刪除已接收的檔案。 |
| 服務維運人員 | 調查環境配置、容量及清理方面的故障；使用診斷紀錄，而非 worker 的暫存檔。 |

在這個託管範例中，平台團隊負責操作 control plane、runtime 和儲存服務。Lamp 專案負責人提供測試用的 issue 資料，並決定哪些呼叫者可以執行及審查 Lamp 工作。請參閱[部署模式](../design/deployment-patterns.md)，了解改由他人操作 worker 時，責任如何調整。

下一篇：[Sandbox 生命週期](sandbox-lifecycle.md)逐一說明服務在每次狀態變更時會保留及刪除哪些資料與資源。
