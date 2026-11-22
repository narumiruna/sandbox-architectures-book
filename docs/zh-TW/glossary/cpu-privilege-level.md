# CPU privilege level

CPU privilege level 決定程式碼可在處理器上直接執行哪些操作。在 x86-64 上，[作業系統 kernel](kernel.md) 通常在權限最高的 ring 0 執行，而應用程式則在 ring 3 的 [user space](user-space.md) 執行。[System call](system-call.md) 讓應用程式能請求 kernel 執行操作，而不必取得 ring 0 權限。

## 範例

當 Linux 應用程式開啟檔案時，處理器從 ring 3 切換到 ring 0，開始執行 kernel 的 system call 處理程式。Kernel 檢查請求，並將結果傳回在 ring 3 的應用程式。

## Guest 內的權限

[Intel VT-x](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) 將 [guest](guest.md) 執行（VMX non-root operation）和 [host](host.md) 執行（VMX root operation）分開。兩者都可以使用 ring 0 和 ring 3。在 ring 0 的 guest kernel 比自己的應用程式有更高的權限，但仍在 guest 模式下執行。從 guest ring 3 切換到 guest ring 0 並不是 [VM exit](vm-exit.md)。

[返回詞彙表](../glossary.md)
