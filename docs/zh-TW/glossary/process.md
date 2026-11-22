# Process

Process 是程式正在執行的實例。[native binary](native-binary.md) 是系統可以執行的檔案；process 則是系統啟動該程式後實際執行的實例。同一個程式執行兩次，使用的記憶體、開啟的檔案和權限都可能不同。

## 範例

Agent 啟動 Lamp 的測試執行器時，作業系統會啟動一個可要求開啟 `total.c` 的 process。這個 process 透過 [system call](system-call.md) 向 [kernel](kernel.md) 要求執行該操作。如果用不同的 sandbox 設定再次啟動同一個測試執行器，它能看到的檔案也可能不同。

## 何時需要留意

在 [operating-system process sandbox](operating-system-process-sandbox.md) 中，host kernel 會對執行中的 process 強制套用限制。測試執行器可以啟動其他 process，稱為 child processes。請確認這些限制也適用於它們，而且它們只會繼承所需的資料和已開啟的檔案。相較之下，[virtual machine](virtual-machine.md) 內的 process 使用的是 VM 自己的 kernel。

請參閱 [Sandbox isolation boundaries](../sandbox-isolation-boundaries.md#follow-a-request-to-open-a-file)，瞭解開啟檔案的請求會經過哪些環節。

[返回詞彙表](../glossary.md)
