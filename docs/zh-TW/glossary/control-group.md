# Control group (cgroup)

Control group（簡稱 cgroup）將 Linux 行程分組，讓作業系統能量測或限制它們使用的資源，例如 CPU 時間和記憶體。Cgroup 不決定這些行程可以開啟哪些檔案，或可以連到哪些網路目的地。

## 範例

建置 sandbox 將編譯器和它的工作行程放在同一個 cgroup 中。服務可以量測整個工作的記憶體用量，並設定上限，避免工作用盡機器的記憶體。

## Linux 如何管理群組的資源

在 [Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) 中，群組排列成樹狀結構。*Controllers* 是 [kernel](kernel.md) 中負責管理這些群組特定資源的部分。例如，CPU controller 可以限制群組的 CPU 時間，memory controller 則可以追蹤群組的記憶體用量並強制執行上限。

使用 [namespaces](namespace.md) 分隔各自可見的資源，再用另一套 [policy](policy.md) 控制檔案和網路存取。這些控制措施的用途不同於資源用量統計和限制。

[返回詞彙表](index.md)
