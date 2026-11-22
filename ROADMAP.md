# Sandbox Architectures Book：寫作路線圖

這是一本學習沙箱技術的書，也是一份選型指南。它要回答兩個問題：**沙箱靠什麼限制程式？理解這些原理後，怎麼判斷哪種技術適合自己的工作？** 讀者不只要會照著範例做，還要能解釋某個方案為什麼有效、有哪些限制，以及什麼情況下需要換架構。

本書寫給想認識沙箱技術或需要設計、採用及審查沙箱的讀者；不需要先懂虛擬化。[書籍導覽](docs/index.md)從基礎概念與隔離機制開始，再用同一個案例練習設計、設定存取規則、維運與驗證；真實實作集中在參考篇，供選型時查閱。英文是原稿與預設版本。多語言版本在第一個完整英文版本之後推出，不是該版本的交付條件。這份路線圖依交付順序排列，不設定日期。

## 目前進度

`[x]` 表示已完成；`[ ]` 表示尚待完成。

- [x] **基礎：** [隔離邊界](docs/sandbox-isolation-boundaries.md)、[術語表](docs/glossary.md)、[clone 後帶讀](README.md#read-a-local-copy-with-a-coding-agent)
- [x] **選型：** [三種情境的 Lamp 選型紀錄與公開產品案例](docs/practice/design/choosing-a-sandbox.md)
- [x] **權限與維運：** [權限、資料流與選型紀錄範本](docs/practice/design/from-issue-to-patch.md)
- [x] **驗證：** [存取測試](docs/practice/verification/verifying-access-rules.md)、[量測](docs/practice/verification/measuring-a-sandbox.md)、[實作評估](docs/agent-sandbox-architectures.md#how-to-evaluate-a-candidate)
- [x] **遷移：** [雙租戶隔離、容量和切換演練及實測結果](docs/practice/operations/scaling-a-sandbox.md)

- [x] **多語言版本：** [台灣正體中文](docs/zh-TW/index.md)、[日文](docs/ja/index.md)、[韓文](docs/ko/index.md)均已涵蓋全書 87 頁。見[章節翻譯進度](#章節翻譯進度)。
- [x] **擴充案例：** [為需要下載套件的 CI 工作設定對外連線](docs/practice/data-and-access/network-policy.md#case-a-ci-job-that-needs-packages)。

本機演練使用假資料與程序沙箱；不是對正式 VM 或服務的驗證。

## 第一階段：建立基礎知識，理解隔離原理

- [x] **從程式如何使用資源開始。** 用「程式開啟檔案」說明程序、作業系統核心及系統呼叫；再區分政策（允許什麼）與隔離機制（由誰強制限制）。
- [x] **用同一組問題認識六種隔離方式。** 分別追蹤原生程式透過作業系統介面存取資源，以及腳本透過執行環境呼叫工具的路徑。每種方式都說明：哪個元件處理請求、哪些資源仍然共用、哪些工作跑得動、隔離不涵蓋什麼。
- [x] **把原理連到真實實作。** 說明容器映像如何封裝程式、執行環境如何隔離程式，以及控制平面如何管理環境。讓讀者遇到新產品或新技術時，能辨認它改變的是哪一層，而不是只記住名稱。

閱讀入口：[隔離邊界](docs/sandbox-isolation-boundaries.md)先建立概念，再對照[程序沙箱](docs/isolation/native-programs/operating-system-process-sandboxes.md)與 [WebAssembly](docs/isolation/generated-scripts/webassembly.md) 如何處理程式的請求。

### 讓術語隨手可查

- [x] **在閱讀當下就找得到。** 各章第一次使用重要術語時，用一句白話定義並直接連到詞條。從[術語表](docs/glossary.md)查找時，也能用英文全名、常見縮寫或簡稱找到同一頁，例如 `WebAssembly` 和 `Wasm`。
- [x] **詞條先給答案，再補細節。** 每個詞條以一句定義開頭，再解釋作用或原理、說明使用情境，並給一個具體範例。容易混淆的詞要說明差別，並連回相關章節。例如，`control plane` 可以在建置工作結束後清理沙箱，但不是實際攔下讀檔請求的元件。

- [x] **完成條件：** 從隔離章中 `isolation boundary` 和 `policy` 的首次出現處各點一次，就能到對應詞條；架構調查與實務篇也各驗證一個術語首次出現處的連結。從術語表用 `WebAssembly` 或 `Wasm` 查找，都要找到同一頁。抽查的詞條均須包含定義、解釋、使用情境與範例。不熟虛擬化的讀者能說出範例中由誰處理檔案存取、由誰檢查工具權限，以及為什麼用了虛擬機器仍要檢查主機開放了哪些檔案。

### Clone 後與 coding agent 一起學習

把整個儲存庫當成可互動的教材。除了瀏覽網站，讀者也可用 `git clone` 下載書稿，再讓能讀取本機檔案的 coding agent 依照自己的程度帶讀；不綁定特定工具。

- [x] **從 [README.md](README.md) 開始。** 提供 clone 指令、在儲存庫根目錄開始帶讀的步驟，以及可直接使用的提問範例。讓讀者和 coding agent 都知道章節入口、術語表與可執行範例分別在哪裡。
- [x] **以書稿為依據。** 讓 coding agent 指出參考的檔案與小節，遇到術語就帶讀者查詞條，再用一個小問題確認理解。把書中沒有交代的內容明確標示為補充或未知。
- [x] **預設只讀。** 帶讀不必修改書稿或執行指令。需要動手時，先說明要執行什麼、預期看到什麼，再由讀者決定是否執行書中的本機範例。

> 起始提問：我是初學者。請根據 `docs/sandbox-isolation-boundaries.md` 說明 `isolation boundary` 和 `policy` 的差別，附上對應的詞條及書稿路徑，最後問我一題，確認我能把兩者用在檔案存取的例子上。請先不要修改檔案或執行指令。

- [x] **完成條件：** 從一份全新的 clone 開始，讀者能照著 `README.md` 取得有書稿出處的解釋，開啟引用的檔案、小節及詞條，並完成一題理解練習。過程不必建置網站、啟用額外整合、執行書中範例或使用特定 coding agent 的專屬功能。練習後確認儲存庫內沒有新增或修改的檔案。

## 第二階段：寫出可重用的選型方法

### 從個人專案到大型服務

- [x] **小型個人專案：** 確認代理程式需要讀寫哪些本機檔案、是否執行外來程式碼。保護家目錄、憑證與原始工作區，同時讓日常開發保持簡單。
- [x] **公司內部服務：** 確認哪些團隊可以使用哪些儲存庫及內部 API，以及誰管理權限和處理失敗。比較團隊間隔離、身分授權、稽核紀錄與自架或託管的維運成本。
- [x] **大型代理程式服務：** 確認不同客戶同時送件時，哪些資源可共用，以及單次工作失敗或超量會影響誰。比較客戶間的資料隔離、工作清理、資源配額、尖峰排隊時間與每次工作的成本。

規模不是隔離強度的替代指標。個人專案如果會執行外來程式碼，也可能需要嚴格隔離；大型服務則不必讓只做查詢的工作取得完整的開發環境。

- [x] **對照公開產品流程：** [CodeRabbit 審查既有的 pull request（PR）](https://docs.coderabbit.ai/overview/pull-request-review)，以及 [GitHub Copilot cloud agent 接手開發任務並提出新的 PR](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github)。先比較兩種工作需要的輸入、工具權限與輸出，再查證官方文件是否公開執行環境、隔離範圍與資料保留方式。產品功能不等於內部架構；未公開的部分標成未知，不拿來推定技術選擇。

### 選型步驟

- [x] **列出必要條件。** 要跑的是受限腳本，還是需要原生程式、編譯器及子程序？誰能提供程式碼？要保護哪些資料？工作可否與主機或其他工作共用作業系統核心？
- [x] **先選隔離方式，再比較實作。** 如果只需透過一個唯讀工具查工單，先評估限制工具呼叫的腳本環境，並確認工具本身有授權檢查。如果必須執行原生程式且不能共用主機核心，即使程序沙箱啟動更快，也不符合條件；這時可先評估虛擬機器。另外決定部署在哪裡（本機或雲端）、由誰維運（自架或託管）；這兩件事不直接決定隔離方式。
- [x] **決定哪些工作共用一個隔離環境。** 除了隔離機制，也要決定 [isolation unit](docs/glossary/isolation-unit.md)。例如，同樣使用 VM，可以每次工作開一台新的 VM，也可以讓同一租戶的多項工作重用一台 VM。說明哪些工作可以共用、哪些狀態可保留、哪些資料必須清除。
- [x] **比較符合條件的候選方案。** 用同一個工作比較相容性、端到端耗時、資源用量與維運成本。分清楚哪些有官方文件佐證、哪些已實測，以及哪些仍未知。

- [x] **完成條件：** 把同一張 Lamp 工單放進上述三種情境，讓讀者看出工作不變時，哪些條件會因使用者、資料與共用方式而改變。每個情境都附一份簡短的選型紀錄：必要條件、所選隔離機制、哪些工作共用一個環境、重用時保留與清除的狀態、選擇與排除其他方案的理由，以及何時要重新評估。公開產品案例另用來說明不同工作流程如何改變需求，不當作同一項工作的效能比較。

## 第三階段：把選型連到權限與維運

延續同一張工單，說明怎麼從「選了哪種邊界」走到「這個環境實際能做什麼」。代理程式只讀取必要的工單資訊，在獨立環境中修改與測試原始碼副本，只交出修補檔和測試紀錄供人審查；沒有發布權限。

- [x] **資料與存取：** 說清楚程式可以呼叫哪些工具、讀寫哪些工作區、存取哪些網路端點，憑證放在哪裡，以及誰可以讀取輸出。說明如何讓不同租戶的資料不互通。
- [x] **維運：** 區分限制程式行為的執行邊界，以及負責建立、設定與清理沙箱的控制平面。交代資源超限、工作失敗或環境重用時，誰負責處理、哪些資料會留下。

- [x] **完成條件：** 讀者能從書籍首頁沿著工單範例，追蹤每一步的權限與資料流，並能在選型紀錄中寫出允許的存取、負責人和清理規則。

## 第四階段：用實驗驗證選擇

先用隔離原理預測結果，再動手驗證。不要把尚未驗證的必要條件當成已滿足；任一必要條件未達成，就調整設定或改選其他方案。

- [x] **驗證存取規則：** 用假資料和本機測試服務，同時檢查「應允許的動作成功」與「應拒絕的動作確實因規則而失敗」。例如，工作程式能讀自己的測試檔，但不能寫入唯讀工作區或讀取另一個工作的測試檔。
- [x] **量測實際工作：** 用同一份小型工作負載，分開記錄從啟動到收到第一筆指令輸出的耗時，以及從啟動到工作完成的耗時。註明測試環境、快取狀態及量測範圍，不把單次結果當成產品排名。
- [x] **補齊重做所需資訊：** 為可執行範例寫明前置條件、指令、預期結果及限制，並維持架構調查的評估小節與驗證章之間的連結。範例只檢查本機的程序沙箱，不能替代對虛擬機器或實際部署環境的驗證，也不需要真實憑證或外部服務。

- [x] **完成條件：** 另一位讀者能在文件指定的環境重做範例，辨認哪些規則已測、哪些沒有測。各章已完成導覽註冊，內部連結、嚴格建置與 `prek` 檢查均通過；新增或修改的 Mermaid 圖也已在窄螢幕上確認可讀。

## 第五階段：從小型服務遷移到大型服務

用 Lamp 示範從單一使用者到公司多團隊，再到不同客戶共用服務。重點不是一步換成大型平台，而是知道這次要解決的是容量問題，還是原本的隔離假設已經不成立。

- [x] **先辨認必須改的部分。** 如果只是排隊變久，先量測是執行容量、環境啟動，還是其他環節拖慢工作；只加容量不一定要換隔離技術。若開始接收不同客戶的程式碼或私有資料，則要先驗證租戶之間的隔離與授權，不能等用量成長後再補。
- [x] **拆開共用狀態與權限。** 列出舊服務依賴的本機狀態、共用目錄與憑證。明確區分接收、排程與記錄工作的控制平面，以及執行工作的環境。由控制平面驗證呼叫者身分，並判定每項工作所屬的團隊或租戶。界定工作區、憑證、快取和產物可以在哪個範圍共用，並指派清理責任。
- [x] **分批切換，先訂好回復條件。** 先用測試資料驗證隔離、重試與清理，再從少數內部團隊試辦，逐批把新工作導到新環境；讓舊工作在原環境完成，不搬執行中的沙箱。事先訂好排隊時間、完成率和每次工作成本的目標，以決定何時擴大試辦或暫停。若失敗，可暫停接收或退回仍符合隔離要求的方案，不能為了回復服務而把新租戶導回不符合要求的舊環境。

- [x] **完成條件：** 用測試資料演練切換，並交付兩組結果：
  - [x] **隔離與清理。** 在試辦環境用兩個測試租戶執行同一項 Lamp 工作。用不同的測試標記確認每項工作掛載的是自己租戶的工作區，且看不到另一個租戶的標記；各租戶能取回自己的修補檔與測試紀錄，而讀取對方產物的請求會因存取規則被拒絕。另確認取消工作後會清理該工作區。
  - [x] **容量與切換。** 用相同的測試工作負載、送件速率及並行需求比較舊環境與試辦環境。記錄排隊時間、完成率與每次工作成本，對照事先設定的目標。綜合隔離檢查與容量量測，說明何時只需加容量、何時須更換隔離或授權方式，以及何時擴大試辦、暫停或退回仍符合隔離要求的環境。

達成五個階段，即可交付本書第一個完整版本。

## 後續：按讀者需求擴充

### 多語言版本

- [x] **預設語言：** 英文（`en`）是目前的預設語言，也是後續翻譯的對照基準。
- [x] **新增首批翻譯：** 每種語言均包含首頁、隔離邊界章、術語表和全部詞條。
  - [x] 台灣正體中文（`zh-TW`）
  - [x] 日文（`ja`）
  - [x] 韓文（`ko`）
- [x] **翻譯版保留英文專有名詞。** 各語言版的正文與詞條都沿用同一套英文術語、產品名稱和縮寫。詞條以英文術語為標題，定義、解釋、使用情境與範例的說明文字使用該版本的語言。
- [x] **完成條件：** 讀者能在同一章的已翻譯版本之間切換，點英文術語即可讀到所選語言的解釋。還沒有翻譯時，明確標示並提供英文原文連結。已驗證產生的語言與詞條連結，並在窄螢幕上測試切換、英文原文連結與圖表。

後續新增或更新譯文時，遵循 [翻譯版維護規則](README.md#translation-editions)。

#### 章節翻譯進度

台灣正體中文、日文及韓文各有 87 頁，與英文原稿一一對應。以下 22 頁的 66 個譯本均已補齊並在 `zensical.toml` 登錄。

- **Foundations（6 頁）**
  - [x] [Hardware-backed virtual machines](docs/isolation/native-programs/hardware-backed-virtual-machines.md)
  - [x] [User-space kernels](docs/isolation/native-programs/user-space-kernels.md)
  - [x] [Operating-system process sandboxes](docs/isolation/native-programs/operating-system-process-sandboxes.md)
  - [x] [WebAssembly](docs/isolation/generated-scripts/webassembly.md)
  - [x] [Engine isolates](docs/isolation/generated-scripts/engine-isolates.md)
  - [x] [Restricted interpreters](docs/isolation/generated-scripts/restricted-interpreters.md)
- **Design a sandbox（3 頁）**
  - [x] [From issue to patch](docs/practice/design/from-issue-to-patch.md)
  - [x] [Choosing a sandbox](docs/practice/design/choosing-a-sandbox.md)
  - [x] [Deployment patterns](docs/practice/design/deployment-patterns.md)
- **Set access rules（5 頁）**
  - [x] [Tool authorization](docs/practice/design/tool-authorization.md)
  - [x] [Workspaces and artifacts](docs/practice/data-and-access/workspaces-and-artifacts.md)
  - [x] [Network policy](docs/practice/data-and-access/network-policy.md)
  - [x] [Credentials and identity](docs/practice/data-and-access/credentials-and-identity.md)
  - [x] [Multi-tenant isolation](docs/practice/data-and-access/multi-tenant-isolation.md)
- **Operate a sandbox（4 頁）**
  - [x] [Control planes](docs/practice/operations/control-planes.md)
  - [x] [Sandbox lifecycle](docs/practice/operations/sandbox-lifecycle.md)
  - [x] [Resource limits](docs/practice/operations/resource-limits.md)
  - [x] [Observability and debugging](docs/practice/operations/observability-and-debugging.md)
- **Verify a sandbox（2 頁）**
  - [x] [Verifying access rules](docs/practice/verification/verifying-access-rules.md)
  - [x] [Measuring a sandbox](docs/practice/verification/measuring-a-sandbox.md)
- **Grow a sandbox service（1 頁）**
  - [x] [Grow a sandbox service](docs/practice/operations/scaling-a-sandbox.md)
- **Reference（1 頁）**
  - [x] [Agent sandbox architectures](docs/agent-sandbox-architectures.md)

### 持續擴充內容

- [x] **先補會改變設計決策的案例。** 在 [CI 套件下載案例](docs/practice/data-and-access/network-policy.md#case-a-ci-job-that-needs-packages)中，只有下載服務能對外連線；工作程式從準備好的套件快取安裝，維持離線。

擴充架構調查時，只有當新實作能說明不同的隔離方式、共用範圍或維運取捨才納入。用官方文件或原始碼支持實作細節，必要時標明版本或修訂，並區分文件描述與實測結果。

不以收齊所有產品、做通用效能排名，或證明某一種架構絕對安全為目標。
