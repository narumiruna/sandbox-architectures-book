# Windows Hypervisor Platform (WHP)

Windows Hypervisor Platform（WHP）是 Windows 的程式設計介面，讓 [virtual machine monitor (VMM)](virtual-machine-monitor.md) 可以使用 host 的硬體虛擬化功能。WHP 是 [host](host.md) 上的介面，不是 VMM、底層的 [hypervisor](hypervisor.md)，也不是 VM 內執行的 kernel。

## 範例

測試服務在 Windows 上使用 NVX 執行 Linux [microVM](microvm.md) sandbox。Host 端的 VMM 使用 WHP 執行 VM。Sandbox 內的測試程式仍然向 Linux [guest kernel](guest.md) 要求開啟檔案和啟動程式，而不是向 Windows API 提出這些要求。

## Windows 介面提供什麼

[Microsoft WHP API](https://learn.microsoft.com/en-us/virtualization/api/) 讓 host 程式建立 *partition*（供 guest 使用的隔離環境）、設定其記憶體，以及建立並執行虛擬處理器。[API 定義](https://learn.microsoft.com/en-us/virtualization/api/hypervisor-platform/hypervisor-platform) 說明這些操作，以及呼叫者如何檢查平台支援的功能。VM 的設定和裝置行為仍由 VMM 提供。

例如，[NVX 在 `42f413d` 修訂版的 Windows/WHP 需求](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#windows--whp) 要求在 host 韌體中啟用硬體虛擬化，在 Windows 中啟用 Windows Hypervisor Platform 功能，然後重新開機。請勿將這個 API 與 Linux host 介面 [KVM](kernel-based-virtual-machine.md) 和 [MSHV](microsoft-hypervisor.md) 混淆。

[返回詞彙表](index.md)
