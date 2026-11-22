# Namespace

Namespace 讓一組 Linux processes 有自己的系統資源檢視，例如 process ID、已掛載的檔案系統或網路介面。讓 processes 使用不同的 namespaces 並不表示它們有各自的 [kernels](kernel.md)。

## 範例

測試 sandbox 使用 mount namespace，讓測試執行程式在 `/workspace` 看到專案目錄，但看不到 host 的家目錄。另一個獨立的 [process ID namespace](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html) 讓測試執行程式看到本次工作的 processes，但看不到 host 上無關的 processes。

## 獨立的檢視不是權限規則

Linux 針對不同資源提供[不同類型的 namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)。改變掛載內容不會讓 workload 擁有獨立的網路檢視。若權限允許，透過可寫入 [mount](mount.md) 共用的檔案仍可修改。

Namespaces 決定 processes 能看到什麼。以路徑為依據的存取控制決定 processes 能對檔案做什麼，[seccomp](seccomp.md) 篩選 system calls，而 [control groups](control-group.md) 記錄或限制資源用量。

[返回詞彙表](index.md)
