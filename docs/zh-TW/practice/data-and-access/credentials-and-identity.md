# Credentials 與身分 {#credentials-and-identity}

如果工作只需要執行一項獲准的操作，就只讓它執行該操作，不要交給它 [credential](../../glossary/credential.md)（用來證明身分或取得存取權的值）。在 [Lamp 操作範例](../design/from-issue-to-patch.md)中，host 的處理函式會讀取本機測試資料，不需要服務 credential。服務會在指令碼和 worker 之外確認請求者的身分。這兩個程式都不會取得請求者的 credentials，也不會取得 repository、issue 儲存區或審查儲存區的任何 credentials。

收集程式使用自己的服務身分寫入審查儲存區。審查人員使用另一個身分讀取已接收的輸出。這兩個身分都不能透過這個工作流程發布修正。

## 變化情境：遠端 issue 儲存區 {#variant-a-remote-issue-store}

如果日後用遠端 issue 儲存區取代本機測試資料，就讓 host 的處理函式充當中介，也就是代替呼叫端執行獲准請求的可信任元件。處理函式使用外層服務確認的身分，而不是採信指令碼聲稱的專案名稱。它會用自己權限範圍有限的 credential 發出請求，並只傳回獲准的欄位。如果處理函式接受任何 issue 請求，光把 credential 藏起來也沒有用。

如果透過檔案或環境變數傳入 credential，程式碼就能複製它。縮短有效期限只能限制 credential 可用的時間，無法防止副本出現在記錄或已儲存的狀態中。在這種做法中，credential 只保留在處理函式內，不會放進任一 runtime 的檔案或環境變數。

### 追蹤預留值的流向 {#follow-the-placeholder}

1. 虛構的 issue 儲存區提供一個假 credential 給處理函式，以 `<ISSUE_READ_GRANT>` 表示。處理函式位於指令碼和 worker 的邊界之外。這項授權只允許讀取 Lamp 的 `LAMP-17`，並在核發五分鐘後到期。它不能用來讀取 Cedar 的 issue、修改 issue 或發布 repository 的變更。
2. 處理函式會先確認呼叫端有權查詢，再使用這項授權。它會直接拒絕未獲授權的請求，不會聯絡儲存區。儲存區會檢查授權範圍和到期時間。授權到期時，處理函式會捨棄它；之後若要查詢，必須重新檢查授權，並取得新的授權憑證。
3. 驗證範圍內的查詢在到期前能成功，且儲存區會拒絕已到期的授權。使用這個假值，檢查傳回的 issue 資料、worker 的設定和檔案、修補檔、測試輸出，以及各處的記錄（包括處理函式的記錄）是否有洩漏。也要檢查儲存下來的 [snapshots](../../glossary/snapshot.md)，包括擷取的記憶體內容（如果有）。即使檔案已移除，記憶體 snapshot 仍可能留有副本。請在掛接工作資料前擷取 worker 的 snapshots，不要在處理函式持有 credentials 時擷取它的狀態。

下一步：[多 tenant 隔離](multi-tenant-isolation.md)說明在哪些地方要再次執行這些存取檢查，以免 Lamp 和 Cedar 讀取彼此的資料。
