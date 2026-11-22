# Credential

Credential 是服務用來確認請求者身分或存取權限的資料。例如，API token 是程式可傳給服務以取得存取權的值。如果 sandbox 中的程式碼取得可重複使用的 credential，就可能用它執行原本預期的單一操作以外的操作。

## 範例

Sandbox 需要一筆 issue 的標題。在 sandbox 外執行的 [tool](tool.md) 會檢查該 issue 是否屬於核准的專案。Tool 將唯讀 token 傳給 issue tracker，再將標題傳回 sandbox。Token 由 tool 和 issue tracker 處理；sandbox 中的程式碼只會收到標題。

## 誰可以使用

任何取得有效 [bearer token](https://www.rfc-editor.org/rfc/rfc6750.html#section-1.2) 的人，都可以在服務接受該 token 的地方使用它。如果 sandbox 中的程式碼能從檔案或程式設定讀取 token，就可以直接使用它。Token 的副本也可能留在日誌中，或出現在儲存程式記憶體的 [snapshot](snapshot.md) 中。

採用 [least privilege](least-privilege.md)：優先使用有效期短的 credential，只授予任務所需的操作和資源存取權。如果程式碼只需要結果，不需要 credential，可透過 host tool 或 [credential injection](credential-injection.md) 讓程式接觸不到 credential。

[返回詞彙表](index.md)
