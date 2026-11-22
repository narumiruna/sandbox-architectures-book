# 擴充 sandbox 服務 {#grow-a-sandbox-service}

如果有工作正在排隊等待 worker，就增加容量。如果新使用者和新資料無法再安全地沿用原本的共用方式，就調整 [isolation boundary](../../glossary/isolation-boundary.md) 或 [authorization](../../glossary/authorization.md)。這是兩項不同的決策。如果服務會把某位客戶的檔案交給另一位客戶，增加 worker 也無法解決問題。

要做的事不變：[查詢 Lamp 的 issue `LAMP-17`、修正 C 程式，並傳回文字格式的修補檔和測試記錄供審查](../design/from-issue-to-patch.md)。Worker 無法發布成果。隨著服務使用者增加，需要做以下調整：

| 階段 | 可以共用什麼 | 增加使用者前必須調整什麼 |
| --- | --- | --- |
| 個人專案 | 所有工作都由同一位開發者擁有。各項工作可以使用同一套唯讀的編譯器，但各自編輯用完即丟的副本。 | 先量測工作在哪個階段等待，再增加 worker。如果有其他人可以提供程式碼、測試或指示，就重新檢視邊界。 |
| 內部服務 | 受信任的團隊可以共用服務，以及裝有乾淨編譯器的唯讀檔案系統。不共用團隊的私人儲存庫、建置輸出或服務憑證。 | 驗證呼叫者的身分，將每項工作對應到所屬團隊，並分別檢查 issue、原始碼和輸出的存取權。在這個設計中，每次嘗試都使用一台全新的 [virtual machine (VM)](../../glossary/virtual-machine.md)。 |
| 對客戶提供服務 | 不同客戶屬於不同的 [tenants](../../glossary/tenant.md)。共用唯讀基礎映像和已驗證的公開相依項目，但不共用可寫入檔案、私人快取項目或憑證。 | 開放客戶使用前，驗證 tenant 的指派和相關限制是否確實執行。限制每個 tenant 可同時執行的工作數，以免單一客戶的工作量突然增加時占滿所有 worker 名額。 |

## 將狀態與執行分開 {#separate-state-from-execution}

列出舊服務原本假設都放在本機的項目：簽出的原始碼、暫存檔、快取的相依項目、查詢 issue 用的憑證，以及已儲存的修補檔和記錄。記下 worker 需要哪些項目、哪些項目應移到 worker 之外。使用 [Lamp 決策記錄](../design/from-issue-to-patch.md#fill-in-your-decision-record)，為每個項目指定負責人和清理規則。

| 資源 | 試辦期間由誰控管 | 保留期限與共用方式 |
| --- | --- | --- |
| 工作記錄 | [Control plane](../../glossary/control-plane.md) 驗證呼叫者身分、確認成員資格、指派 tenant、將工作排入佇列，並記錄每次嘗試。提供專案 ID 或工作 ID 並不能證明成員資格。 | 重試時沿用工作 ID 和 tenant ID，但每次嘗試都會取得新的 ID。記錄狀態和時間，不記錄憑證。 |
| Workspace 與執行 | Control plane 選取該 tenant 在固定修訂版本的原始碼，並將全新副本附加到 worker。VM 和設定的 [mounts](../../glossary/mount.md) 限制 worker 可存取的範圍。 | 每次嘗試都使用新的 workspace。工作成功、失敗或取消時，先停止 worker，再移除它的副本。如果清理失敗，先隔離 worker 並重試清理，不要重新指派它。 |
| 身分與相依項目 | 查詢 issue 的 tool 檢查 tenant，只傳回 Lamp 需要的欄位。試辦用的 worker 採離線建置，不會取得任何 [credentials](../../glossary/credential.md)。 | 將 issue 服務的憑證一律留在 worker 之外。只共用乾淨、唯讀的公開輸入。日後如果加入私人快取項目，就按 tenant 分別授權。 |
| 修補檔與測試記錄 | 工作成功時，由 worker 外部的收集程式接收預定的兩項 [artifacts](../../glossary/artifact.md)。每次擷取資料時，存放審查資料的儲存區都會確認經身分驗證的 tenant 和審查權限。 | 將成功產生的輸出保留到約定的到期時間。工作取消或失敗時，不要發布或傳輸不完整的輸出。 |

## 使用虛構的 tenant 演練 {#rehearse-with-fake-tenants}

這項本機演練使用 [Bubblewrap](https://github.com/containers/bubblewrap) 執行 process worker；它仍與 host 共用 [kernel](../../glossary/kernel.md)。演練使用虛構身分、位於記憶體中的審查資料儲存區、與[驗證練習](../verification/verifying-access-rules.md)相同的 C workload，以及兩個試行 worker 名額，而不是一個。演練會實際檢查這個設定下的 workspace 可見範圍和清理結果。不會測試 guest kernel、身分提供者、持久性儲存區或正式環境的容量。只使用提供的測試資料：示範用的收集程式並未設計成能處理惡意輸出。

請依照[驗證存取規則](../verification/verifying-access-rules.md)所列的 Linux、Bubblewrap、Python 和 C 編譯器先決條件準備環境。安裝 [uv](https://docs.astral.sh/uv/getting-started/installation/) 後，在儲存庫根目錄執行：

```sh
uv run --offline --no-project --python /usr/bin/python3 python -B examples/rehearse_migration.py
```

1. **檢查隔離與清理。** 兩個虛構的 tenant 都執行 `LAMP-17`。各自的 workspace 在相同路徑放有不同的標記。Host 會確認另一個標記確實存在，但各 worker 必須只能看到自己的標記。每個 tenant 都必須能擷取自己的修補檔和測試記錄；即使另一個 tenant 知道工作 ID，審查資料儲存區也必須拒絕它存取。演練會啟動一個額外的 worker，在出現部分輸出後將它取消，確認它的 workspace 已移除，再用全新的 workspace 重試。
2. **在相同條件下比較容量。** 將相同的十二項工作分別送入兩個 worker 集區，每隔 10 ms 送出一項（每秒提交 100 項），不等待前面的工作完成。兩次測試使用相同的測試資料和 process 邊界，並先預跑一次，不重複使用 workspace 或建置輸出。唯一改變的是 worker 名額。排隊時間從提交工作起算，到分配到的名額開始執行為止，不含後續的環境設定；p95 是第 95 百分位數（此處取十二項工作中最長的排隊時間）。只有成功傳回結果的工作才算完成。成本模型按量測期間的所有名額計費，每個名額每小時 $0.06，再除以成功工作數。這不是實際帳單，也不包含持續運作的基礎設施、儲存或網路流量。
3. **決定是否切換。** 演練在執行前設定以下示範目標：p95 排隊時間最多 400 ms、十二項工作全部成功，而且每項成功工作的估算成本最多 $0.000020。如果隔離或清理失敗，演練會在測試容量之前停止。如果試行環境有任何一項未達標，就不開放 Cedar 使用。如果兩道關卡都通過，Cedar 的新工作會在試行環境執行，已在舊環境開始的 Lamp 工作則留在原處直到完成。演練也會檢查暫停規則：等現有工作都結束後，只有 Lamp 可以回到舊環境。

### 結果範例 {#example-results}

在一次 Linux 測試中（WSL2 x86-64、AMD Ryzen 9 7950X3D、kernel 6.18.33.2、Bubblewrap 0.11.1、GCC 15.2.0），Lamp 和 Cedar 都只能看到自己的標記，也只能擷取自己的修補檔和記錄。取消額外的工作後，它的 workspace 已移除；重新嘗試後也傳回了預期的輸出。

| 集區 | 排隊時間中位數 | p95 排隊時間 | 完成數 | 每項成功工作的估算成本 |
| --- | ---: | ---: | ---: | ---: |
| 舊環境，一個名額 | 358.6 ms | 710.6 ms | 12/12 | $0.00000124 |
| 試行環境，兩個名額 | 117.6 ms | 243.9 ms | 12/12 | $0.00000115 |

*在這台 host 上*，增加名額就足以達到排隊時間目標。但這並未驗證目標 VM 設定，也不代表舊環境可作為 Cedar 的備援。開放客戶使用前，請在預計採用的環境中重新檢查。

## 分批切換新工作 {#switch-new-jobs-in-batches}

1. 先拆解各階段的等待時間，再調整設定。如果佇列變長，但 worker 的執行速度符合預期，試著在相同的安全 policy 下增加名額。如果時間主要花在啟動環境或建置，先[量測該階段](../verification/measuring-a-sandbox.md)，再增加容量。如果新 tenant 無法沿用舊有的 kernel、mounts 或儲存區權限，即使佇列是空的，也要先修正這些邊界。
2. 在目標環境中用虛構 tenant 執行檢查和重試演練，不要使用正式環境的客戶資料。對於 VM 設計，先使用測試用的 control plane，並為兩個測試 tenant 各準備全新的離線 VM。在允許共用 host 的情況下，將兩者的 VM 放在同一台測試執行機上，並在那裡檢查 workspace 和輸出路徑。使用測試帳號，在實際執行身分驗證與授權的邊界上檢查身分。先就排隊時間、完成情況和成本目標達成共識，再開始試辦。從少數核准的內部團隊開始，只有在檢查通過且持續達標時才分批擴大。將新工作導向新環境，讓已開始的工作留在原處完成。不要移動執行中的 worker，也不要將舊 workspace 附加給新的 tenant。
3. 如果存取、清理或容量有任何一項未通過檢查，就暫停接收新工作。只有在舊環境仍符合這些工作目前的隔離與授權要求時，才能將工作導回舊環境。如果舊服務只支援單一擁有者，就不能當作客戶工作的備援。先保留或拒絕這些工作，直到有符合要求的環境可用。
