# Tool 的授權 {#tool-authorization}

指令碼可以使用某個 [tool](../../glossary/tool.md)，但這不代表它的每次呼叫都通過 [authorization](../../glossary/authorization.md)。在 [Lamp 操作範例](from-issue-to-patch.md)中，指令碼可以呼叫一個唯讀的 issue tool，但 [host](../../glossary/host.md) 會檢查每項請求。指令碼可以讀取 Lamp 的 issue `LAMP-17`，但不能讀取 Lamp 的其他 issue，也不能讀取 Cedar 的 issue。

## 指令碼可以呼叫哪些 tool？ {#which-tools-can-the-script-call}

Host 在 [restricted interpreter](../../glossary/restricted-interpreter.md) 中執行查詢指令碼。Tool 的 [allowlist](../../glossary/allowlist.md) 只包含 `get_issue`，這項操作接受專案和 issue ID。指令碼沒有 shell，不能直接存取檔案系統，也不能任意連線到網路。它不會取得建置或發布用的 tool。獨立的 Linux worker 會編譯和測試 Lamp 程式，但不會取得 issue tool。

這份清單限制指令碼可以要求哪些操作，但不決定某項獲准的操作可以讀取哪個專案。即使操作是唯讀的，也可能把資料透露給無權讀取的呼叫端。

## 一次呼叫能做什麼？ {#what-can-one-call-do}

實作 `get_issue` 的 [host function](../../glossary/host-function.md) 在 interpreter 外執行。Host 會將這次執行已核准的範圍交給函式：讀取 Lamp 的 `LAMP-17`。指令碼傳入的引數只用來指定目標，不會授予存取權。處理函式會先檢查操作、專案和 issue 是否在允許的範圍內，再查詢紀錄。它會同時使用獲准的專案和 issue ID 來讀取本機測試資料。Issue ID 的前綴不能證明該 issue 屬於哪個專案。

- **允許：** `get_issue(project="Lamp", issue="LAMP-17")` 只會傳回 issue 的標題和關於總數計算錯誤的回報，不會傳回任何 [credentials](../../glossary/credential.md) 或其他紀錄。
- **拒絕：** `get_issue(project="Cedar", issue="CEDAR-9")` 不會通過專案檢查，因此不會讀取 Cedar 的測試資料，也不會透露該 issue 是否存在。
- **不得改用其他查詢範圍：** `get_issue(project="Lamp", issue="CEDAR-9")` 不會通過這次執行的 issue 檢查。如果 tool 改為允許讀取整個專案，它仍必須只搜尋 Lamp，並回報找不到符合的紀錄；不得改為搜尋所有專案。

將傳回的 issue 文字視為資料。即使回報中有一句話要求指令碼讀取另一個專案，也無法改變 host 提供的權限。

## 單獨檢查處理函式 {#check-the-handler-on-its-own}

準備兩個專案的假紀錄，並在只允許讀取 Lamp 的 `LAMP-17` 的情境下直接測試 host 的處理函式。確認獲准的呼叫只傳回預期欄位，而查詢任一專案的其他 issue 都會在查詢前遭到拒絕。這項測試不依賴 interpreter，驗證的是這個處理函式，而非其他介面的存取檢查。[本機存取檢查](../verification/verifying-access-rules.md)示範較簡單的專案層級規則，不需要使用實際運作的 issue 追蹤系統。

下一步：[Workspace 與 artifact](../data-and-access/workspaces-and-artifacts.md)會說明原始碼副本如何進入 worker，以及兩個文字檔如何從 worker 傳出。
