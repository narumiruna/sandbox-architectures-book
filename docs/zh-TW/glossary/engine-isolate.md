# Engine isolate

Engine isolate 是語言引擎內的獨立執行環境。語言引擎是執行 JavaScript 等語言程式碼的軟體。每個 isolate 都有自己的狀態，包括其中的指令碼建立的物件。多個 isolate 可以共用同一個作業系統行程，因此 isolate 並不是獨立的行程或 [virtual machine](virtual-machine.md)。

## 範例

Issue tracker 在不同的 isolate 中執行兩個團隊的指令碼。一個指令碼可以在記憶體中保留一份 issue 標題清單，而另一個指令碼看不到它。為了取得標題，每個指令碼都會呼叫 [host function](host-function.md)，由它檢查該指令碼獲准讀取哪個專案。

## 引擎狀態與 host 存取

[V8 13.8.258 Isolate API](https://github.com/v8/v8/blob/13.8.258/include/v8-isolate.h#L277-L285) 規定各自的狀態必須分開：一個 isolate 的 V8 物件不得在另一個 isolate 中使用。這種分隔由引擎管理。嵌入引擎的應用程式稱為 [host](host.md)，由它決定指令碼能呼叫哪些操作。[Cloudflare 的 Dynamic Workers 架構](https://blog.cloudflare.com/dynamic-workers/) 說明了這項區別：呼叫端可以提供具名介面，讓指令碼存取選定的服務，同時封鎖直接向外送出的請求。

Isolate 不會限制 host function 代替指令碼執行的操作。請依照指令碼的權限檢查每項對外提供的操作，並確認平台如何限制 CPU 和記憶體用量。如果任務需要執行原生程式，請使用支援這類程式的獨立環境，例如 [operating-system process sandbox](operating-system-process-sandbox.md)。

[返回詞彙表](index.md)
