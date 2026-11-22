# Egress

Egress 是跨過 sandbox 邊界向外傳送的網路流量。Egress [policy](policy.md) 可以限制 sandbox 能聯絡哪些外部服務。但允許連到某個服務，本身不會限制 sandbox 在該服務上能執行哪些操作。

## 範例

Sandbox 執行的測試會從測試伺服器讀取範例記錄。Gateway 允許讀取這些記錄，但封鎖修改記錄或聯絡其他服務的請求。請求送出 sandbox，回覆則傳回 sandbox。

## 對外規則在哪裡生效

防火牆可以依照網路位址和連接埠的 [allowlist](allowlist.md) 控管流量。如果規則必須區分讀取和寫入，請使用能讀取請求的元件，例如 web proxy，或直接在服務端限制操作。可信任的元件必須在相關路徑上強制執行規則；單靠 proxy 設定無法限制直接連線。

請分開檢查網路存取權和透過 [tool](tool.md) 提供的操作。即使無法直接存取網路，sandbox 仍可能呼叫 host tool，由它代為送出請求。該 tool 需要有自己的 authorization 檢查。

## 連線與回覆

對外請求的回覆是 [ingress](ingress.md) 流量，因為它們進入 sandbox。網路控制措施可以允許 sandbox 主動建立的連線接收回覆，同時不讓外部用戶端建立新連線。當叢集的網路軟體強制執行 [Kubernetes 1.35 network policies](https://github.com/kubernetes/website/blob/03c191bcc446f9c15a9e68d6cd1154b53bde4291/content/en/docs/concepts/services-networking/network-policies.md#the-two-sorts-of-pod-isolation) 時，這些 policies 就是這樣運作的。

[返回詞彙表](index.md)
