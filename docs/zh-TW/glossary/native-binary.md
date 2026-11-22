# Native binary

Native binary 是編譯成特定處理器可執行的指令，並針對特定作業系統介面的程式。它需要相容的環境。Linux native binary 不是 [WebAssembly](webassembly.md) 模組，也不能直接當成這類模組執行。

## 範例

程式碼審查 sandbox 執行一套已針對 64 位元 Arm Linux 建置的 linter。具有該處理器架構和必要程式庫的 Linux [virtual machine](virtual-machine.md) 可以執行它。若要直接在 Wasm runtime 中執行 linter，服務會提供 Wasm 版本，而非 Linux 執行檔。

## 相容性取決於什麼

執行檔格式告訴作業系統如何載入程式。例如，Linux [ELF 執行檔](https://man7.org/linux/man-pages/man5/elf.5.html)會記錄其目標處理器架構。如果程式使用共用程式庫，環境還需要相容的[載入器和程式庫](https://man7.org/linux/man-pages/man8/ld.so.8.html)。執行程式所用的 kernel 介面也必須支援該程式的 [system calls](system-call.md)。僅有相符的處理器還不夠。

[返回詞彙表](../glossary.md)
