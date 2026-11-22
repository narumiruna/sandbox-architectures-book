# User space

User space 位於作業系統的 [kernel](kernel.md) 之外，是應用程式和大部分服務執行的地方。比起 kernel，user space 中的程式較難直接控制硬體和系統資源。應用程式通常就在 user space 執行，但這本身並不表示程式受到 sandbox 限制。

## 範例

編輯器和測試執行器都可以在同一台 Linux 機器的 user space 執行。編輯器可以讀取使用者有權存取的個人檔案。Sandbox 允許測試執行器讀取專案，卻不允許它讀取這些個人檔案。限制來自 sandbox，而不是來自在 user space 執行。

## 程式如何向 kernel 要求服務

程式需要開啟檔案或執行其他 kernel 操作時，會發出 [system call](system-call.md)，通常是透過函式庫。[Linux system call 簡介](https://man7.org/linux/man-pages/man2/intro.2.html) 說明 kernel 如何處理請求並傳回結果。[user-space kernel](user-space-kernel.md) 則是在 host kernel 外部以軟體實作該介面。

[返回詞彙表](index.md)
