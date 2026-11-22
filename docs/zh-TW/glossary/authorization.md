# Authorization

Authorization 是判斷身分已知的呼叫端是否可對特定資源執行某個動作。必須先確認呼叫端的身分；知道身分並不代表授予存取權限。

## 範例

指令碼可以呼叫查詢議題的 [tool](tool.md) 來讀取 `LAMP-17`，但不能讀取另一個專案的議題。每次收到請求時，工具都會檢查身分已知的呼叫端具備哪些權限，以及請求指定哪個議題。請求欄位填了另一個專案，並不能證明呼叫端有權存取。

## 何時需要檢查

如果一項作業可以代替呼叫端傳回資料或做出變更，就要檢查 authorization。[Sandbox](sandbox.md) 可以限制指令碼能呼叫哪些工具，但每個工具仍須檢查該呼叫端能做什麼。完整範例請參閱 [工具的 authorization（英文）](../../practice/design/tool-authorization.md)。

[返回詞彙表](../glossary.md)
