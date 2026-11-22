# 測量 sandbox 的執行時間 {#measuring-a-sandbox}

記下呼叫端何時看到第一筆輸出，**以及**工作何時完成。Worker 可能很快就有回應，但要再花很長時間才能編譯、測試並寫出結果。比較時間之前，先[驗證存取規則](verifying-access-rules.md)；再快的 worker，只要無法強制執行某項要求，就不列入考量。

## 每次使用相同的 workload {#use-the-same-workload-each-time}

[Workload](../../glossary/workload.md) 是 sandbox 執行的程式碼與 process。本練習使用存取檢查中的 [Lamp 任務](../design/from-issue-to-patch.md)。它會修正 `total.c` 副本中誤用減法的錯誤，用 GCC 建置 C 程式，確認二加三等於五，再寫出修補檔與測試紀錄。每次都在相同的 [Bubblewrap process sandbox](../../isolation/native-programs/operating-system-process-sandboxes.md) 中執行同一組測試材料，不呼叫服務，也不刻意加入延遲。

| 測量項目 | 停止計時的時點 |
| --- | --- |
| 到第一筆輸出的時間 | 呼叫端收到 `LAMP-17: loaded` 時。Worker 讀完測試材料後、開始編譯或測試修正前，會輸出這一行。 |
| 到工作完成的時間 | 呼叫端讀完 worker 的輸出，並確認它已結束時。成功的執行會建置程式、執行測試，並寫入 `change.patch` 和 `test.log`。 |

兩項計時都在 host 啟動 Bubblewrap 前一刻開始，因此都包括建立 process sandbox 和啟動 Python 所需的時間。計時**不包括**啟動前準備輸入和輸出目錄、執行後檢查 artifact 和刪除工作區，以及任何遠端排隊或 artifact 傳輸。在部署環境中，如果這些階段會增加使用者的等待時間，也要測量。

## 啟動十次，每次都用新的環境 {#run-ten-fresh-launches}

使用[驗證存取規則](verifying-access-rules.md#run-the-local-checks)列出的 Linux、Bubblewrap、Python、GCC 和 `uv` 先決條件。從本書版本庫工作副本的根目錄執行：

```bash
uv run --offline --no-project --python /usr/bin/python3 python -B examples/lamp/lab.py measure
```

預期會看到十列，每列有兩個以毫秒為單位的時間值（`first_output_ms` 和 `completion_ms`），最後列出每個測量項目的最小值、中位數和最大值。每次啟動時，執行程式都要求結束狀態碼為零、兩行預期輸出皆出現，並且產生預期的修補檔和紀錄。任何一次執行失敗，練習就會停止，不會回報該次啟動的時間。

每次啟動都使用新的輸入副本、輸出目錄和 sandbox。沒有持久保留的建置快取，也沒有清除或追蹤 host 的檔案系統快取。後續啟動可以從快取讀取先前讀過的編譯器或函式庫。使用新的 sandbox，不代表 host 的快取是冷的。如果要比較另一個候選方案，請記錄 host、kernel、工具版本、runtime policy、並行程度，以及如何準備或重複使用工作區和快取。

## 判讀一組測量結果 {#interpret-one-run}

其中一組測量在 WSL2 的 Ubuntu 26.04.1 LTS 上依序執行了十次（Linux 6.18.33.2、x86-64、AMD Ryzen 9 7950X3D，host 暫存檔放在 `tmpfs`），使用 Bubblewrap 0.11.1、Python 3.14.4 和 GCC 15.2.0。執行程式建立了新的工作區。這組測量前已執行存取檢查，沒有清除或追蹤 host 快取。

| 測量項目 | 中位數 | 最小值至最大值 |
| --- | ---: | ---: |
| 到第一筆輸出的時間 | 24.37 ms | 21.49–26.48 ms |
| 到工作完成的時間 | 62.23 ms | 58.47–63.94 ms |

呼叫端看到第一行輸出時，距離工作完成還有一段時間。從數值範圍可看出，即使是這麼小的任務，也不能只靠一次啟動來描述它的表現。這是測量方法的範例，不是效能基準，也不是產品排名。

評估實際的候選方案時，請固定 workload，並說清楚啟動包含哪些工作：[cold start](../../glossary/cold-start.md)、從 [warm pool](../../glossary/warm-pool.md) 取得已分派的執行環境，以及從 [snapshot](../../glossary/snapshot.md) 還原，所做的工作並不相同。本範例未測量任何 VM 或 warm pool、記憶體、磁碟用量、負載下的啟動時間或 artifact 傳輸。若要測量 worker 的記憶體用量峰值，請用專用的 [control group](../../glossary/control-group.md) 或等效的後端用量統計，不要用單一 process 的 [resident set size](../../glossary/resident-set-size.md) 峰值。請參閱 [Sandbox 生命週期](../operations/sandbox-lifecycle.md)，了解服務可重複使用哪些狀態，並參閱[候選方案評估清單](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)，了解還有哪些項目要比較。

接下來：[擴充 sandbox 服務](../operations/scaling-a-sandbox.md)會比較排隊時間，並用兩個測試 tenant 演練切換。
