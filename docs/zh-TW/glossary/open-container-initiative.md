# Open Container Initiative (OCI)

[Open Container Initiative](https://opencontainers.org/) 維護封裝、散布和執行 containers 的開放規格。符合 OCI 規格可讓不同工具互通，但無法據此判斷透過什麼機制將執行中的程式與 host 隔開。

## 範例

建置服務將編譯器和測試工具打包成 OCI [container image](container-image.md)。只要兩種後端都支援該 image 及其中的程式，服務就可用相同的 image 啟動測試 sandbox，不論是共用 host kernel，還是使用 [virtual machine](virtual-machine.md)。

## 各項規格涵蓋什麼

[Image Specification v1.1.0](https://github.com/opencontainers/image-spec/tree/v1.1.0) 定義檔案系統變更和設定如何封裝。[Distribution Specification v1.1.0](https://github.com/opencontainers/distribution-spec/tree/v1.1.0) 定義工具如何將內容傳入及傳出 registry（儲存 container images 的服務）。[Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/tree/v1.2.1) 定義執行已備妥 container 所需的設定和生命週期。若要了解程式碼可存取哪些資源，請檢查所選的 [container runtime](container-runtime.md) 及其設定。

[返回詞彙表](../glossary.md)
