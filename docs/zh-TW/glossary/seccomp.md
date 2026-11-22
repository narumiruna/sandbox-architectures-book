# Seccomp

Seccomp 是 Linux 的功能，可篩選 [system calls](system-call.md)，也就是程式送給 kernel 的請求。它可以封鎖特定類型的請求，但無法單獨依照路徑名稱強制執行檔案存取規則。

## 範例

文件轉換 sandbox 可以用 seccomp 封鎖建立網路通訊端的請求。只封鎖建立操作，不會限制程式使用它已有的通訊端。另行設定檔案系統 policy，才能限制轉換程式從哪裡讀取輸入檔案，以及將結果寫到哪裡。

## 篩選器能檢查什麼

[Linux seccomp 篩選器文件](https://docs.kernel.org/userspace-api/seccomp_filter.html) 說明，篩選器可以檢查 system call 編號和原始引數值。它可以允許呼叫，或讓呼叫直接失敗而不執行。傳給 `openat` 等呼叫的檔案路徑，是存放在程式記憶體中的文字。篩選器看到的是文字的位址，而不是文字本身。

請用 [mounts](mount.md) 控制哪些檔案可見，再用檔案存取規則控制可對檔案執行的操作。[control group](control-group.md) 處理的是另一件事：量測或限制資源用量。

[返回詞彙表](index.md)
