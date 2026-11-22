# 選擇 sandbox {#choosing-a-sandbox}

選擇 [sandbox](../../glossary/sandbox.md) 時，要看程式必須做什麼，以及哪些東西不能讓它碰到。服務的規模無法告訴你邊界需要多強。個人專案也可能執行不受信任的程式碼，大型服務也可能有只需讀取 issue 的工作。

## 從需求到決策紀錄 {#from-requirements-to-a-decision-record}

搭配 [Lamp 決策紀錄範本](from-issue-to-patch.md#fill-in-your-decision-record)使用這套方法。

1. **列出哪些操作必須可行，以及哪些東西必須隔絕。** 記錄誰可以提供或變更 [workload](../../glossary/workload.md)，包括原始碼、測試、建置指示，或 [agent](../../glossary/agent.md) 產生的指令。列出所需的檔案、操作和連線。決定工作能否共用 [host](../../glossary/host.md) 的 [kernel](../../glossary/kernel.md)（也就是其作業系統的核心），或與其他工作共用 kernel。
2. **先選擇 [isolation boundary](../../glossary/isolation-boundary.md)，再挑產品。** [Restricted interpreter](../../glossary/restricted-interpreter.md) 可以讓指令碼存取一個唯讀的 [tool](../../glossary/tool.md)。Tool 仍會對每項請求執行 [authorization](../../glossary/authorization.md) 檢查。如果 worker 必須執行編譯器和子 process，卻不能使用 host kernel，[operating-system process sandbox](../../glossary/operating-system-process-sandbox.md) 就不符合需求。如果 worker 需要自己的 Linux kernel，請評估 [virtual machine (VM)](../../glossary/virtual-machine.md)。至於[在哪裡執行、由誰維運](deployment-patterns.md)，則另行決定。
3. **選擇 [isolation unit](../../glossary/isolation-unit.md)，也就是決定哪些工作共用同一個環境。** 例如，每項工作使用一台全新的 VM，與同一位客戶重複使用一台 VM，這兩種做法的邊界類型相同，但共用規則不同。記錄哪些東西可以保留、哪些必須移除，以及工作成功、失敗或取消後，由誰驗證清理結果。
4. **先驗證是否符合需求，再比較成本或速度。** 使用相同的原始碼修訂版本、測試和工具鏈。確認允許的操作能成功，禁止的操作也確實因預期的原因而失敗。只比較符合需求的候選方案。測量從提交工作到輸出可供審查的時間，包括排隊和設定的時間；記錄 CPU、記憶體及磁碟用量、快取狀態，以及每項工作產生的營運成本。測試前先設定目標。逐項標記需求的驗證狀態：**有文件佐證**、**已實測**或**未知**；未知不算通過。請參閱[評估候選方案](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate)和[衡量 sandbox](../verification/measuring-a-sandbox.md)。

## 同一個 Lamp 任務的三種決策 {#three-decisions-for-the-same-lamp-task}

在三種情境中，[Lamp 任務](from-issue-to-patch.md)都會讀取 `LAMP-17`，修正小型 C 程式算錯總數的問題，編譯修正後的程式，並測試兩個項目加上三個項目是否等於五個。查詢指令碼在 restricted interpreter 中只使用一個唯讀的 issue tool。獨立的 Linux worker 在修訂版本已知、用完即丟的 [workspace](../../glossary/workspace.md) 中編輯。Worker 不需要網路存取、issue tool 或 repository 的 [credentials](../../glossary/credential.md)。供審查的 [artifacts](../../glossary/artifact.md) 只有 `change.patch` 和 `test.log`；只有獲得授權的審查人員可以讀取，且檔案在七天後到期。Worker 無法發布成果。下列紀錄是設計提案，不是測試結果。

### Linux 工作站上的個人專案 {#personal-project-on-a-linux-workstation}

- **需求：** 開發者啟動工作，但不信任 agent 的指令。Worker 及其子 process 不得讀取開發者的家目錄或 credentials，也不得變更原始簽出目錄。這個專案可以接受共用工作站的 kernel。
- **邊界與隔離單位：** 在 operating-system process sandbox 中執行原生工具。建置和測試共用同一個 sandbox，但只限於這次執行。
- **保留與清理：** 重複使用已安裝的唯讀工具鏈，不重複使用 worker 或先前的建置目錄。停止 process tree 中的所有 process，移除暫存副本和建置檔案。將兩個輸出留在開發者限制存取的審查目錄，到期為止。
- **為什麼選這個方案：** 一般 shell 不提供這類檔案限制。另用一個 guest kernel 則會增加這個專案不需要的設定工作。
- **何時重新評估：** 外部貢獻者可以提供建置內容或測試，或工作站不能再與 worker 共用 kernel 時。

### 供公司內多個團隊使用的內部服務 {#internal-service-for-several-company-teams}

- **需求：** 團隊成員可以變更建置內容和測試。Worker 不得共用 host 或其他工作的 kernel。讀取 issue、掛接 workspace 或讀取 artifact 前，先檢查呼叫端的團隊和專案。記錄誰啟動了工作、專案和修訂版本，以及執行結果。平台團隊負責處理失敗的執行及清理工作。
- **邊界與隔離單位：** 每次執行都在內部 runner 上啟動一台全新的 Linux VM。即使是同一個團隊接連執行的工作，也不共用 guest。
- **保留與清理：** 重複使用含編譯器但不含團隊資料的唯讀基礎映像。銷毀 guest，捨棄它的暫存空間和建置檔案。稽核紀錄和兩個僅限該團隊存取的輸出，分別依各自的保留規則保存。
- **為什麼選這個方案：** 使用 host kernel 的 process sandbox 不符合 kernel 必須分開的規則。如果一個團隊重複使用同一台 VM，就必須在兩次執行之間重設 VM 並驗證結果。起初先不重複使用，以免失敗的工作留下檔案，讓重試的工作讀到。
- **何時重新評估：** 服務需要內部 API、開始接受非員工提供的程式碼，或未達排隊時間目標時。確認問題是缺少存取控制，還是單純因為 worker 不足。

### 供彼此無關的客戶使用的大型服務 {#large-service-for-unrelated-customers}

- **需求：** 任何已註冊的客戶都可以提供程式碼。[Tenant](../../glossary/tenant.md) 是指資料和工作必須與其他客戶分開的客戶。任何工作都不得與 host 或其他工作共用 kernel。在查詢 issue、掛接 workspace 及擷取 artifact 時，分別強制執行 tenant 的存取規則。套用 [resource limits](../../glossary/resource-limit.md)，並為每個 tenant 設定可同時執行的工作數量上限：超過上限的工作必須等待或會遭拒絕，但只要還有可用容量，其他 tenant 仍可啟動工作。
- **邊界與隔離單位：** 為每項工作啟動一台全新的 Linux VM，並將它指派給單一 tenant。只有 policy 允許時才共用 runner 的硬體；客戶的工作絕不共用同一個 guest。
- **保留與清理：** 重複使用不含客戶資料的唯讀基礎映像。不重複使用仍在執行的 guest 或客戶快取。即使工作取消，也要捨棄 guest 和暫存空間。將修補檔和測試輸出保存在僅限該 tenant 存取的審查儲存空間，到期為止；重試時使用全新的儲存空間。
- **為什麼選這個方案：** 使用 host kernel 的 process sandbox 和共用 guest 都不符合 kernel 的規則。每個 tenant 使用一台 VM，雖然能在 guest 邊界分隔不同 tenant，但同一個 tenant 的工作仍可能影響彼此的狀態。獨立的 VM 無法修正 issue tool 或儲存服務的設定錯誤。
- **何時重新評估：** 在尖峰負載下，排隊時間、完成率或每項工作的成本未達目標時。如果瓶頸是 runner 的執行名額，就增加容量。如果共用 host 的前提有變，就重新評估邊界或執行位置。允許任何形式的重複使用前，先驗證後續工作能看到哪些資料。

使用[無害的存取檢查](../verification/verifying-access-rules.md)來測試應該允許和拒絕的存取路徑，並以 [tenant 隔離檢查](../data-and-access/multi-tenant-isolation.md)測試共用服務。本機檢查無法證明 VM 或服務確實強制執行這些規則。

## 兩種公開的工作流程，兩套不同的需求 {#two-public-flows-different-requirements}

[CodeRabbit Pull Request Reviews](https://docs.coderabbit.ai/overview/pull-request-review) 的起點是一份已經在 pull request（PR）中提出的變更。[GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github) 可以從一項開發任務開始，並提出新的 PR。這是兩種不同的工作，不是效能基準測試，也不是 Lamp 的兩種實作。比較只涵蓋這兩種流程，不包括 CodeRabbit Coding Agent、Copilot code review 或其他模式。比較依據是 2026 年 11 月 22 日查閱的官方文件，而非產品測試。

| 檢查項目 | CodeRabbit：審查既有 PR | GitHub Copilot cloud agent：實作任務並提出 PR |
| --- | --- | --- |
| 輸入與輸出 | 開啟 PR 或推送新的 commit 都可以觸發自動審查。CodeRabbit 會使用變更內容、相關的 repository 脈絡，以及連結的 issue（如有），並把發現的問題和建議發在既有的 PR 上。 | 在 Agents 分頁選取 repository，請 Copilot 實作任務並開啟 PR。[指派 issue](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github#assigning-an-issue-to-copilot)是另一個起點：Copilot 會收到 issue 的標題、說明、既有留言，以及任何額外指示。它為新的 PR 製作變更，再由人員審查。 |
| Tool 與權限 | Linter 等[分析工具](https://docs.coderabbit.ai/tools/index)會提供分析結果。例如，其 [ESLint 整合](https://docs.coderabbit.ai/tools/eslint)只允許使用核准的外掛。審查流程不需要新分支，但[安裝 GitHub App](https://docs.coderabbit.ai/platforms/github-com#review-permissions) 會要求對程式碼、PR 和檢查項目的讀寫權限。App 的權限並不能說明每個分析工具實際取得哪些權限。 | Copilot 可以在 repository 的副本上執行指令和測試。針對新 PR，[GitHub 文件](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations#copilot-cloud-agent-can-push-code-changes-to-your-repository)說明呼叫端需要 repository 的寫入權限，而 Copilot 只能推送到它獲指派的分支，不能核准或合併該 PR。 |
| 環境與隔離 | CodeRabbit [說明其雲端 sandbox](https://docs.coderabbit.ai/overview/architecture) 會複製完整的 repository 以供分析。架構圖列出了 [Cloud Run](https://docs.cloud.google.com/run/docs/about-execution-environments)，而 Cloud Run 不只一種執行環境。查閱過的資料無法確認適用的隔離邊界，也無法確認哪些執行工作或客戶可以共用運作中的環境或實體 host。 | 針對 **Cloud** 選項，GitHub [說明每個 session 都有一個 Linux sandbox](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/about-cloud-sandboxes)，與使用者的電腦和其他 session 隔離，且可設定網路限制。這無法確認底層使用的邊界技術，也無法確認誰可以共用實體 host。 |
| 保留的資料 | CodeRabbit 的文件說明，它預設會啟用可重複使用的原始碼和相依套件[快取](https://docs.coderabbit.ai/reference/caching)，並在七天內到期。其 [FAQ](https://docs.coderabbit.ai/faq#data-security) 說明另有保留時間較長的審查脈絡資料。快取到期不代表所有審查資料都會在同一期限內刪除。 | [Session 資料](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/session-data)文件說明，Cloud session 停止後會儲存 [snapshot](../../glossary/snapshot.md)，以便恢復檔案並繼續未完成的工作。查閱過的資料無法確認所有副本何時刪除。PR 和 commit 仍與 worker 的狀態分開。 |

**注意適用範圍。** GitHub 也有 **Actions** 環境的文件。對於由 GitHub 代管的 Actions session，結束時會銷毀 session 環境，但會保留記錄。不要把這條清理規則或任何 Actions runner 的特性套用到預設的 **Cloud** 選項。

評估代管服務時，請針對選用的模式、方案和設定查閱文件。記錄哪些東西可以跨越邊界，以及執行結束後可能留下什麼。如果必要的特性沒有文件佐證，請向供應商索取證據，並盡可能用假資料驗證。不要只看到「sandbox」一詞，就推定它使用 VM、每項工作都有全新的環境，或所有資料都會完整刪除。

下一步：[部署模式](deployment-patterns.md)會說明如何將隔離方式的選擇，與執行位置、權責和清理的決策分開考量。
