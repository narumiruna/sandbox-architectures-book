# Microsoft Hypervisor (MSHV)

Microsoft Hypervisor 是控制 guest 作業系統如何使用實體電腦的軟體。本書以 *MSHV* 指稱 Microsoft Hypervisor 的後端；在支援的 Linux host 上，[virtual machine monitor (VMM)](virtual-machine-monitor.md) 可透過 `/dev/mshv` 存取這個後端。該裝置是 host 介面，不是 [guest kernel](guest.md)，也不是 VMM 本身。

## 範例

建置服務透過 NVX 在啟用 MSHV 的 Linux host 上執行 Linux [microVM](microvm.md) sandbox。Host 上的 VMM 使用 `/dev/mshv` 執行 VM。在 VM 內，建置工具仍向 guest 自己的 Linux kernel 要求開啟檔案和執行程式。

## 哪裡可以使用 Linux 介面

[Microsoft Hypervisor 規格](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/tlfs)將它的隔離執行環境稱為 *partitions*。*Root partition* 是具特殊權限的環境，負責管理電腦，並在其中執行虛擬化堆疊。[修訂版 `42f413d` 的 NVX Linux/MSHV 需求](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#linux--mshv)要求 Linux 使用啟用 MSHV 的 kernel，在該 root partition 中執行。該 kernel 必須提供 `/dev/mshv`，且 VMM 必須有該裝置的讀寫權限。在 hypervisor 下執行的一般 Linux guest 不符合這項需求。

不要將這個 Linux 後端與 [Windows Hypervisor Platform (WHP)](windows-hypervisor-platform.md) 或 [KVM](kernel-based-virtual-machine.md) 混淆。WHP 是 VMM 可在 Windows 上使用的 host API，而 KVM 是另一種 Linux host 介面。

[返回詞彙表](../glossary.md)
