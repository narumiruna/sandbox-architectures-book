# Ingress

Ingress 是跨越 sandbox 邊界、進入其中的網路流量。Ingress [policy](policy.md) 可以規定誰能主動連線到內部服務。預覽 URL 讓瀏覽器有路徑可連線到服務，但本身不會驗證使用者的身分。

## 範例

開發人員在 sandbox 中啟動網頁伺服器，並開啟網站預覽。Sandbox 外部的閘道會檢查開發人員是否已登入，以及是否有權存取該 sandbox。閘道只將請求轉送到預覽用的網頁伺服器，不會把登入用的 [credential](credential.md) 傳入 sandbox。

## 路由與存取檢查

如 [RFC 9110 第 3.7 節](https://www.rfc-editor.org/rfc/rfc9110.html#section-3.7) 所述，閘道可以充當 *reverse proxy*：接收用戶端的網頁請求，再轉送到選定的伺服器。路由決定要連到哪個 sandbox 和服務；授權則檢查呼叫端是否有權存取。要讓閘道確實執行授權決定，務必讓服務只能透過這條會檢查權限的路徑存取。

確認路徑會開放哪些服務，以及何時關閉。預覽路徑不必開放 sandbox 中的其他服務，並應在工作階段結束時關閉。即使連線由外部用戶端發起，預覽伺服器送出 sandbox 的回覆仍屬於 [egress](egress.md) 流量。

[返回詞彙表](index.md)
