# Mount

Mount 檔案系統或目錄，就是讓其中的檔案在指定路徑可見。*Bind mount* 不需複製檔案或目錄，就能讓它在另一個路徑可見。如果 sandbox 能透過 bind mount 寫入，就能修改原始檔案。

## 範例

程式碼審查 sandbox 在 `/workspace` 看到 host 的專案目錄。服務提供該目錄的唯讀 mount。審查程式可以查看專案，但不能透過 `/workspace` 修改它。程式將報告寫入另一個輸出目錄。

## Workload 能看到哪些檔案

[mount namespace](namespace.md) 可以讓一組 processes 各自有別於其他群組的掛載檢視。Linux 的 [`mount(2)` 文件](https://man7.org/linux/man-pages/man2/mount.2.html)區分 mount 設定與底層檔案系統。唯讀的 bind mount 會阻止透過該 mount 寫入，但不會讓底層檔案透過其他 mounts 存取時也變成唯讀，也不會隱藏檔案內容。只掛載 [workload](workload.md) 需要看到的檔案。

[返回詞彙表](index.md)
