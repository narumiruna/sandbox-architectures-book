# Extended Page Tables (EPT)

Extended Page Tables（EPT）讓 [Intel 處理器](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) 將 [guest](guest.md) 所見的實體記憶體位址轉換成 [host](host.md) 的實體位址。這是位址轉換的第二階段。Page table 記錄一段記憶體對應到哪裡，以及允許哪些存取方式。

## 範例

應用程式從虛擬位址載入資料。Guest 的 page tables 將該位址對應到 guest 實體位址。CPU 接著使用 EPT 找出對應的 host 實體位址。Guest kernel 可以變更自己的 page tables，但無法控制 EPT。另一個 guest 可以使用相同的 guest 實體位址，而不必使用相同的 host 記憶體。

## 誰控制第二階段的對應？

在使用 [KVM](kernel-based-virtual-machine.md) 的 Linux host 上，第二階段的對應由 KVM 設定。Guest 執行時，CPU 會強制執行這一階段的存取權限。KVM 支援哪些位址轉換，請參閱 [KVM 記憶體文件](https://docs.kernel.org/virt/kvm/x86/mmu.html#translation)。

[返回詞彙表](../glossary.md)
