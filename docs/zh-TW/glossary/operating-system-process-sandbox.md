# Operating-system process sandbox

Operating-system process sandbox 直接在 [host kernel](kernel.md) 上執行程式，並使用該作業系統的控制措施來限制程式能存取哪些資源或執行哪些操作。它不會啟動獨立的 [guest](guest.md) kernel。

## 範例

本機的程式碼審查 sandbox 執行 host 上的搜尋工具，讓工具可讀取專案、寫入暫存輸出目錄。這些工具不需要另一套作業系統，但工具本身和它們建立的子 processes 都應受相同限制。

## 搭配使用的控制措施

在 Linux 上，[namespaces](namespace.md) 可以限制 processes 能看到哪些已掛載的檔案系統或網路介面。[Linux 6.12 Landlock 指南](https://docs.kernel.org/6.12/userspace-api/landlock.html#layers-of-file-path-access-rights)所述的路徑規則可限制對檔案階層的操作。[Seccomp](seccomp.md) 可篩選 system calls，而 [cgroups](control-group.md) 則可量測和限制資源用量。這些控制措施無法互相替代。確認 policy 允許哪些操作，也要確認 policy 同時適用於 sandbox 啟動的程式及其子 processes。

[返回詞彙表](index.md)
