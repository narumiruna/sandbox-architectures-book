# 驗證存取規則 {#verifying-access-rules}

確認獲准的操作會成功，遭拒的操作則會**因為規則而失敗**。例如，如果 worker 無法讀取某個檔案，先開放該檔案，證明同一個 worker 能讀取它。否則，輸入錯字或啟動失敗都可能被誤認為規則成功阻擋了操作。

## 預測結果 {#predict-the-results}

本練習使用虛構的 [Lamp 議題處理流程](../design/from-issue-to-patch.md)。它使用本機的 [operating-system process sandbox](../../glossary/operating-system-process-sandbox.md)，而不是流程示範中的虛擬機器。[Bubblewrap 0.11.1](https://github.com/containers/bubblewrap/blob/v0.11.1/README.md) 負責設定邊界；Linux [kernel](../../glossary/kernel.md) 負責強制執行 [policy](../../glossary/policy.md)。建置 C 程式用的是 host kernel，而不是 guest kernel。

[Mount](../../glossary/mount.md) 讓 worker 可以存取 host 路徑。[Namespace](../../glossary/namespace.md) 讓 process 可以從獨立的範圍查看某項資源。開始檢查前，請先預測執行程式每次只改一條規則時，哪些結果會跟著改變：

| 檢查項目 | 套用 worker policy 的預期結果 | 改動一條規則後的對照結果 |
| --- | --- | --- |
| 讀取指定的輸入並寫入結果 | Worker 讀取自己的 Lamp 標記，在私有的暫存空間建置並測試修正，然後儲存 `change.patch` 和 `test.log` | 這些獲准的操作不需要對照 |
| 寫入輸入副本 | 同一項寫入操作會回傳 `EROFS`（唯讀檔案系統），不會在 host 上建立檔案 | 將同一份暫存輸入以可寫入的方式 mount，寫入就會成功 |
| 讀取另一個工作區的 `/lab/other/marker` | 讀取會回傳 `ENOENT`（沒有這個檔案或目錄）；Cedar 並未 mount | Mount 模擬用的 Cedar 工作區後，就能讀取同一路徑 |
| 從 host 的 loopback（`127.0.0.1`）上的測試服務讀取模擬回應 | 連線會回傳 `ECONNREFUSED`（連線遭拒）：worker 的 network namespace 中沒有程式在該連接埠監聽 | 共用網路時，相同位址和連接埠會回傳 `Lamp test service` |

只回應一次的 TCP 服務只繫結到 loopback，連接埠由作業系統選擇。檢查結束時，服務就會關閉。過程不會用到外部服務或真實資料。Linux 的 [network namespaces](https://man7.org/linux/man-pages/man7/network_namespaces.7.html) 會隔開介面、路由和連接埠號碼。這項對照測試的是能否存取 host 上指定的監聽服務，不是測試對外連線的目的地清單或正式環境的網路。

## 執行本機檢查 {#run-the-local-checks}

請在 x86-64 Linux 上使用非 root 帳號。請先準備下列條件：

- Bubblewrap，且系統允許非特權的 user、mount、PID、IPC、UTS 和 network namespace。本練習以 `/usr/bin/bwrap` 0.11.1 版測試。Host 或外層容器可能會阻止建立 namespace。
- 採用合併式 `/usr` 目錄配置的系統，其中 `/bin`、`/lib` 和 `/lib64` 都指向 `/usr` 內的位置。Sandbox 使用 `/usr/bin/python3`（以 Python 3.14.4 測試）和 `/usr/bin/gcc`，並搭配系統的組譯器、連結器及 C 開發標頭檔（以 GCC 15.2.0 測試）。
- 用來執行 host 指令碼的 [uv](https://docs.astral.sh/uv/getting-started/installation/)。下列指令會使用已安裝的 Python，略過專案設定，且不會下載套件。

從本書版本庫工作副本的根目錄執行：

```bash
uv run --offline --no-project --python /usr/bin/python3 python -B examples/lamp/lab.py verify
```

預期會看到八行 `PASS`，最後一行是：

```text
PASS: Lamp compiled and passed its test; change.patch and test.log verified
```

確認回傳了 **`EROFS`**、**`ENOENT`** 和 **`ECONNREFUSED`**，且各自的對照操作都成功。Bubblewrap 設定出錯代表實驗失敗，不是操作遭拒的證據。如果 host 阻止建立 namespace，或沒有符合要求的目錄配置，請改用相容的 Linux 測試系統。不要為了讓範例通過而移除隔離選項、修改 host 的安全設定，或以 root 身分執行。

在 [Ubuntu WSL2 測試系統](measuring-a-sandbox.md#interpret-one-run)上，八項檢查全數通過。執行程式確認輸入 `total.c` 未變更、`change.patch` 將減法改成加法，而且 `test.log` 包含 `PASS: total(2, 3) = 5`。之後它丟棄了暫存檔案。[測試材料和執行程式的原始碼](https://github.com/narumiruna/sandbox-architectures-book/tree/main/examples/lamp)位於 `examples/lamp/`。

## 判讀證據 {#interpret-the-evidence}

對照操作成功，表示檔案確實存在，而且操作在獲准時可以執行。遭拒的檢查結果顯示，這項設定提供唯讀的 Lamp 輸入給 worker，並隱藏指定的 Cedar 路徑。這並未測試所有路徑、process 或網路路由。Worker 可以讀取已 mount 的 `/usr`，而且仍共用 host kernel。本練習不設定資源上限，也不測試 kernel 抵抗攻擊的能力、繼承的機密資訊、VM 隔離，或正式環境的 tenant 身分。只使用可信任的測試材料。在實際部署中，請用實際的 runtime、mount、身分規則和允許的網路目的地重新執行檢查。請參閱[候選方案評估清單](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)。

## 另行檢查工具授權 {#check-tool-authorization-separately}

Linux 的邊界不決定誰能透過 [host tool](../../glossary/host-function.md) 讀取議題。請獨立測試 [authorization](../../glossary/authorization.md) 處理程式。下列範例使用模擬資料，以及[工具授權](../design/tool-authorization.md)所述較簡單的授權方式，也就是對整個 Lamp 專案授予權限。範例在 Bubblewrap 外執行，不會連接議題追蹤系統。

```bash
uv run --offline --no-project --python /usr/bin/python3 python - <<'PY'
issues = {("Lamp", "LAMP-17"): "Incorrect item total", ("Cedar", "CEDAR-9"): "Dummy issue"}


def lookup_as_lamp_reviewer(project, issue):
    if project != "Lamp":
        raise PermissionError(project)
    return issues[project, issue]


if lookup_as_lamp_reviewer("Lamp", "LAMP-17") != "Incorrect item total":
    raise SystemExit("FAIL: expected the Lamp issue")
for project, issue, expected in (("Cedar", "CEDAR-9", PermissionError),
                                 ("Lamp", "CEDAR-9", KeyError)):
    try:
        lookup_as_lamp_reviewer(project, issue)
    except expected:
        continue
    raise SystemExit(f"FAIL: {project}/{issue} should fail with {expected.__name__}")
print("PASS: authorized lookup, project denial, and no cross-project fallback")
PY
```

接下來：[測量 sandbox 的執行時間](measuring-a-sandbox.md)會為相同的 C workload 計時，但不執行存取測試。
