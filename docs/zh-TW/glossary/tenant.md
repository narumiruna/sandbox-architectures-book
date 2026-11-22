# Tenant

Tenant 可以是使用者、團隊或組織；服務會將其工作或資料與其他 tenant 分開處理。Tenant 表示涉及誰的資源和權限，而不是用什麼方式隔離執行中的程式碼。一個 tenant 可以有多個 sandbox session。

## 範例

建置服務供兩個團隊使用。一個團隊啟動不同的 [sandboxes](sandbox.md)，分別建置函式庫和文件。另一個團隊啟動自己的 sandbox。前兩個 sandbox 屬於同一個 tenant，但第三個不得讀取前兩者的原始碼目錄樹或建置結果。

## 分隔不同 tenant 的資源

[control plane](control-plane.md) 會檢查哪個 tenant 可以啟動或領用 sandbox，以及要掛接哪個 workspace。服務多個 tenant 的 [tool](tool.md) handler 也必須確認呼叫者所屬的 tenant 能使用所要求的資料。它應使用服務提供的身分資訊，而不是把指令碼送來的 tenant 名稱當作使用該 tenant 資源的許可。

Tenant 不一定是 [isolation unit](isolation-unit.md)。服務可以為同一個 tenant 的每項工作提供獨立的 VM，也必須將已儲存的輸出、快取和還原的 [snapshots](snapshot.md) 維持在預定的 tenant 範圍內。如果共用服務會傳回其他 tenant 的資料，使用獨立 VM 也無法解決這個問題。

[返回詞彙表](index.md)
