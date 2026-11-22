# Kernel-based Virtual Machine (KVM)

Kernel-based Virtual Machine (KVM) 是 Linux kernel 的一項功能，透過處理器的虛擬化功能執行 [virtual machines](virtual-machine.md)。它提供介面，讓 [host](host.md) 上的軟體建立和執行 VM。KVM 既不是 [guest kernel](guest.md)，也不是負責管理 VM 及其裝置的完整程式。

## 範例

建置服務在 Linux host 上用 [virtual machine monitor (VMM)](virtual-machine-monitor.md) 執行 Linux sandbox。VMM 使用 KVM 執行 guest 的虛擬處理器，並為建置工作提供虛擬磁碟。建置工具向 guest kernel 發出一般的 Linux 請求，而不是向 host 上的 KVM 發出請求。

## Host 介面

[Linux KVM API](https://docs.kernel.org/virt/kvm/api.html) 說明 VMM 如何開啟 `/dev/kvm`、建立 VM 及其虛擬處理器，以及設定 guest 記憶體。由於各 host 支援的功能不同，VMM 可以查詢有哪些選用功能可用。

VMM 必須能存取 host 上的 `/dev/kvm`。例如，[修訂版 `42f413d` 的 NVX Linux/KVM 需求](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/setup.md#linux--kvm)要求硬體虛擬化及該裝置的讀寫權限。這項權限供 host 端的 VMM 使用，而非供 sandbox 內的 workload 使用。其他 host 介面請參閱 [MSHV](microsoft-hypervisor.md) 和 [WHP](windows-hypervisor-platform.md)。

[返回詞彙表](index.md)
