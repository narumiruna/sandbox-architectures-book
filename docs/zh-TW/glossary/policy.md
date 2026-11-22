# Policy

Policy 是一組規則，規定執行中的程式碼可以採取哪些動作、使用哪些資源。只有受信任的元件套用規則時，規則才有效。給模型的指示本身不是存取限制。

## 範例

Lamp 的測試 [sandbox](sandbox.md) 可以讀取 `total.c` 並寫入暫存輸出，但不能開啟 [host](host.md) 的 SSH 金鑰。在 [process sandbox](operating-system-process-sandbox.md) 中，sandbox 的設定會將專案檔案設為唯讀，並將暫存目錄設為可寫入。Host 的 [kernel](kernel.md) 會依據該設定檢查每項檔案請求，而測試執行程式看不到這些金鑰。

## 為每條規則指定負責執行的元件

[control plane](control-plane.md) 可以在建立 sandbox 時選擇 policy。由 [runtime](runtime.md)、作業系統、proxy 或 [tool](tool.md) 的處理程式各自強制執行自己能觀察到的部分。例如，[Linux kernel 文件](https://docs.kernel.org/userspace-api/seccomp_filter.html)說明，[seccomp](seccomp.md) 可以篩選送到 kernel 的請求，但如果請求只提供檔名在記憶體中的位置，篩選器就不能讀取檔名。對於直接存取檔案的操作，請用檔案系統控制措施強制執行檔案路徑規則。

## 何時需要留意

設定或測試 sandbox 時，請確認在每一道 [isolation boundary](isolation-boundary.md) 上，哪些操作應該成功，哪些應該失敗。如果同一資源既能透過 [mount](mount.md) 存取，也能透過工具存取，請檢查兩條路徑。在一條路徑遭拒，並不代表在另一條也會遭拒。請參閱[追蹤開啟檔案的請求](../sandbox-isolation-boundaries.md#follow-a-request-to-open-a-file)，了解檔案規則的兩個部分。

[返回詞彙表](index.md)
