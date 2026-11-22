# 網路 policy {#network-policy}

在 [Lamp 操作範例](../design/from-issue-to-patch.md)中，worker 不必連線到自身環境以外的任何網路端點，就能完成建置與測試。Issue tool 會讀取 [host](../../glossary/host.md) 上的本機範例紀錄。[Workspace 服務與 artifact 收集元件](workspaces-and-artifacts.md)會透過用完即丟的虛擬磁碟，在執行前傳入資料，並在執行後取出結果；兩者都不需要使用 worker 的網路連接埠。

## 對外連線：只允許必要的目的地 {#outbound-allow-only-required-destinations}

[Egress](../../glossary/egress.md) 是從 worker 邊界送出的網路流量。Host 不會提供 Lamp 的 [virtual machine (VM)](../../glossary/virtual-machine.md) 虛擬網路介面卡。Worker 啟動時就會取得編譯器、原始碼和測試，因此這個設計不需要例外規則。Worker 上的程式碼無法透過 host 的網路連到 issue 儲存服務、相依套件儲存庫、其他 worker 或 control plane。

如果後續的建置需要相依套件，讓獨立的下載服務取得核准的套件，不要開放 worker 的 egress。下方的 CI 案例會說明如何拆分這些權限。如果鏡像站需要驗證身分，請依照[憑證與身分](credentials-and-identity.md)的做法，將身分驗證留在 worker 之外。

如果某個測試變體需要同時測試用戶端和伺服器，可以使用只能從該 VM 內連線的 loopback 端點。`LAMP-17` 的基本版本不使用這類服務。

## 案例：需要套件的 CI 作業 {#case-a-ci-job-that-needs-packages}

假設有一項 [continuous integration (CI) job](../design/deployment-patterns.md#continuous-integration-ci) 負責執行 Lamp JavaScript 版本的測試。它與 `LAMP-17` 不同，需要基礎映像檔裡沒有的套件。作業需要的是這些套件檔案，而不是不受限制的網際網路存取。讓測試 worker 維持離線，只允許下載服務對核准的鏡像站使用 egress。

1. **核准輸入。** 審查 [npm v11.6.2 lockfile](https://github.com/npm/cli/blob/v11.6.2/docs/lib/content/configuring-npm/package-lock-json.md#packages)，其中記錄了套件來源與完整性校驗值。解析完整的相依套件清單，不只處理 Lamp 直接指定的套件。不要把未經審查的修補檔對 lockfile 的變更當成下載新套件的許可。
2. **下載套件時不執行專案程式碼。** 讓下載服務只能向 `deps.lamp.test` 請求核准的封存檔。這是一個虛構的相依套件鏡像站，提供核准套件的副本。鏡像站如需 [credential](../../glossary/credential.md)，就把它留在下載服務內。拒絕其他請求方法、其他套件路徑，以及重新導向未核准的目的地。在準備好封存檔供後續使用之前，逐一比對核准的完整性校驗值。
3. **在邊界內安裝並測試。** 為 worker 準備一份專用的套件快取副本。在這個案例中，使用不需要安裝指令碼的套件。快取完整時，可以讓 [`npm ci`](https://github.com/npm/cli/blob/v11.6.2/docs/lib/content/commands/npm-ci.md#description) 搭配 [`--offline`](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js#L1353-L1361) 和 [`--ignore-scripts`](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js#L860-L872)，依照 lockfile 安裝。仍須在 worker 的邊界封鎖網路存取：這些選項無法限制測試或其子 process 的行為。

分別用完整和不完整的快取檢查這個設計。所有核准的封存檔都存在時，安裝和測試應該成功。若少了一個封存檔，安裝應該失敗，而不是連線到套件登錄服務。另外也要確認下載服務會拒絕未核准的封存檔及內容遭竄改的核准封存檔，而且 worker 無法直接連上鏡像站。這些是 CI 部署的驗收檢查，不是本機 Lamp 練習的測試結果。

## 對內連線：只有需要預覽時才開放 {#inbound-no-access-unless-someone-needs-a-preview}

[Ingress](../../glossary/ingress.md) 是跨過邊界進入的網路流量。沒有虛擬網路介面卡，其他環境就無法連到 worker。`LAMP-17` 的執行環境沒有預覽網址或公開的連接埠。審查者只會連到獨立的審查儲存服務，且仍須取得該服務的授權。

如果後續的 Lamp 工作需要在瀏覽器預覽，請透過閘道開放獨立的預覽服務。閘道會驗證呼叫者的身分，並檢查其是否有權存取該 Lamp session。只在 session 存續期間將流量導向指定的預覽服務。不讓外部存取測試端點及 worker 的其他連接埠。在獲准的預覽連線上回覆，並不代表 worker 有權建立新的對外連線。光有預覽連結不代表有存取權。

透過[存取檢查](../verification/verifying-access-rules.md)，區分預期的流量與 policy 應拒絕的流量。檢查通過只為這些路徑提供證據，不能證明已涵蓋所有網路路徑。

下一篇：[憑證與身分](credentials-and-identity.md)說明如何授權讀取，而不用把服務的機密資料交給 worker。
