# Isolation boundary

Isolation boundary 是將執行中的程式碼與其他程式碼或資源隔開的機制。它可以禁止直接存取，同時提供受控的管道來存取指定資源。邊界是機制；[policy](policy.md) 則規定什麼可以跨越邊界。只知道機制的名稱，無法判斷程式碼能存取什麼。

## 範例

Lamp 的測試工作在以 [virtual machine (VM)](virtual-machine.md) 為基礎的 [sandbox](sandbox.md) 中執行。服務可以把 `total.c` 的副本交給測試執行程式，也可以透過可寫入的共用目錄開放專案。兩種設定都有 VM 邊界，但只有可寫入的共用目錄會讓測試工作直接修改原始檔案。

## 這個機制會隔開什麼

VM 將 guest 作業系統與 [host](host.md) 隔開。[operating-system process sandbox](operating-system-process-sandbox.md) 限制仍使用 host [kernel](kernel.md) 的 [processes](process.md)。語言 [runtime](runtime.md) 則可以限制指令碼只執行指定操作及呼叫指定的 [host functions](host-function.md)。完整比較請參閱 [Sandbox 隔離邊界](../sandbox-isolation-boundaries.md)。

## 何時需要留意

為不受信任的程式碼選擇環境時，先確認必須保護哪些資源、哪個元件負責強制執行 policy，以及該元件開放哪些存取路徑。接著確認 [isolation unit](isolation-unit.md)：同一個 VM 中的兩項工作都在其邊界內，所以這道 VM 邊界不會把兩者隔開。

[返回詞彙表](../glossary.md)
