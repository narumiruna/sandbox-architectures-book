# System call (syscall)

System call（又稱 syscall）是程式向作業系統的 [kernel](kernel.md) 提出的請求。開啟檔案、啟動 process，以及透過網路通訊端傳送資料，都是程式以這種方式要求的操作。

## 範例

建置 sandbox 內的編譯器要求開啟 `/workspace/main.c`。在共用 kernel 的 sandbox 中，host kernel 會依編譯器可見的掛載檔案系統解析該路徑，並檢查編譯器是否有權開啟檔案。如果存取遭拒，請求就會失敗。

## 請求如何處理

如 [Linux system call 簡介](https://man7.org/linux/man-pages/man2/intro.2.html) 所述，程式通常會呼叫函式庫中的函式，再由該函式發出實際的 system call。在共用 kernel 的 sandbox 中，host kernel 處理呼叫，並可使用 [seccomp](seccomp.md) 篩選。在 [virtual machine](virtual-machine.md) 中，由 guest kernel 處理其中程式的呼叫。[user-space kernel](user-space-kernel.md) 可以實作相同的介面，而不必把每個請求直接轉送到 host kernel。

[返回詞彙表](index.md)
