# Allowlist

Allowlist 列出程式可使用的資源或可執行的動作。只有在可信任的元件檢查請求並封鎖不符合清單的請求時，這份清單才會限制存取。

## 範例

建置用的 sandbox 需要下載軟體套件。它的 [policy](policy.md) 只允許 [egress](egress.md) 連線前往團隊的套件鏡像站，也就是存放這些套件副本的伺服器。檢查每條新連線的網路控制機制會執行清單規則；清單本身不會封鎖流量。

## 規則可以比對哪些條件

比對範圍取決於負責檢查的元件能看到什麼。連線規則可以比對目的地和連接埠。會轉送並讀取網頁請求的服務也可以檢查作業和路徑。[OpenShell v0.1.9 的網路規則](https://github.com/NVIDIA/OpenShell/blob/v0.1.9/docs/how-it-works/policies/network-rules.mdx#connection-and-request-checks) 說明了這兩個層級的檢查。

允許連線到某項服務，不會限制 workload 能傳送哪些內容給服務，也不會限制服務接受哪些動作。若 workload 只需要一項作業，為了符合 [least privilege](least-privilege.md)，除了目的地之外也要比對動作。請確認受限制的存取會經過執行該規則的元件；在一條路徑上檢查，並不涵蓋其他路徑。

[返回詞彙表](../glossary.md)
