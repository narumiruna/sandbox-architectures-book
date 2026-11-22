# Agent 的 sandbox 架構 {#agent-sandbox-architectures}

*本調查更新於 2026 年 11 月 22 日。本章比較的是文件所描述的架構，不是實測效能，也不是安全保證。*

本調查比較不同專案如何隔離協助開發的 [agents](glossary/agent.md) 和它們產生的程式碼。

## 執行邊界 {#execution-boundaries}

[Isolation boundary](glossary/isolation-boundary.md) 限制程式可以觸及的範圍。[Policy](glossary/policy.md) 規定哪些項目應可跨越這個邊界。若要瞭解六種隔離方式，請先閱讀 [Sandbox 的隔離邊界](sandbox-isolation-boundaries.md)。

[Virtual machine monitor (VMM)](glossary/virtual-machine-monitor.md) 管理 [virtual machine (VM)](glossary/virtual-machine.md) 和 VM 可見的裝置。VMM 並不是完整的 [sandbox](glossary/sandbox.md) 產品：可由獨立的 [control plane](glossary/control-plane.md) 決定何時啟動 VM，以及要提供哪些資源給它。

## 使用硬體輔助的 Linux 環境 {#hardware-backed-linux-environments}

| 專案 | 提供的功能 | 邊界與範圍 |
| --- | --- | --- |
| [Docker Sandboxes (`sbx`)](https://docs.docker.com/ai/sandboxes/architecture/) | 可直接使用的開發 agent 環境 | 每個本機 sandbox 都在一台 [microVM](glossary/microvm.md) 裡執行，並有自己的 [Docker Engine](https://docs.docker.com/engine/)。哪些資源會被隔離，哪些不會，請參閱 [Docker Sandboxes 案例](#docker-sandboxes)。[本機安裝](https://docs.docker.com/ai/sandboxes/install/)說明 macOS、Windows 和 Linux 的需求。 |
| [libkrun](https://github.com/containers/libkrun) | 可嵌入的 VMM 函式庫，提供 Rust 和 C API | 在 Linux 上使用 [KVM](glossary/kernel-based-virtual-machine.md)，在 Apple silicon 上使用 [Hypervisor Framework](https://developer.apple.com/documentation/hypervisor)。呼叫端決定開放哪些 host 檔案和裝置。[Gondolin](https://github.com/earendil-works/gondolin/blob/main/docs/backends.md) 是一層 sandbox，可用 libkrun 或 QEMU 作為 VMM。 |
| [Cloud Hypervisor](https://github.com/cloud-hypervisor/cloud-hypervisor) | 通用的雲端 VMM | 在 KVM 或 [MSHV](glossary/microsoft-hypervisor.md) 上執行，支援 Linux 和 Windows [guests](glossary/guest.md)。它是後端，不是具有 workspace 和 [credential](glossary/credential.md) policy 的完整 agent sandbox。 |
| [Firecracker](https://github.com/firecracker-microvm/firecracker) | 供 microVM 使用的精簡 VMM | 一般部署是在 Linux 上使用 KVM。上游專案也記載了 [AWS Nitro Sandboxes 後端](https://github.com/firecracker-microvm/firecracker/tree/main/docs/nitro-sandboxes)，這個後端使用 AWS Nitro，而不是 host KVM。 |
| [Kata Containers](https://github.com/kata-containers/kata-containers/blob/main/docs/design/architecture/README.md) | 以 VM 為基礎的 [container runtime](glossary/container-runtime.md) | 在 [Kubernetes](https://kubernetes.io/docs/concepts/overview/) 中，[pod](glossary/pod.md) 在 guest VM 裡執行；同一個 pod 裡的 container 可以共用 guest [kernel](glossary/kernel.md)。Kata [支援多種 VMM](https://github.com/kata-containers/kata-containers/blob/main/docs/hypervisors.md)，包括 QEMU、Cloud Hypervisor 和 Firecracker。Kata 和 Firecracker 屬於不同層，不能直接互相替代。 |
| [Microsoft NVX](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/README.md) | 以 OpenVMM 為基礎的 microVM 技術堆疊和 guest runtime | 文件涵蓋使用 KVM 或 MSHV 的 Linux host，以及使用 [Windows Hypervisor Platform](glossary/windows-hypervisor-platform.md) 的 Windows host。Guest runtime 的設計目標是[每台 Linux microVM 執行一個 workload sandbox](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/design/4-guest-runtime-architecture.md)。 |
| [Apple `container`](https://github.com/apple/container/blob/main/docs/technical-overview.md) | Apple silicon 上的本機 [OCI](glossary/open-container-initiative.md) container 工具 | 透過 Apple 的 [Virtualization framework](https://developer.apple.com/documentation/virtualization)，**每個 container** 各執行一台輕量的 Linux VM。它以 [container images](glossary/container-image.md) 為輸入，但隔離邊界是 VM，而不是 user-space kernel。 |

### Docker Sandboxes：每個 sandbox 一台 VM {#docker-sandboxes}

每個本機 Docker Sandbox 都有自己的 Linux [guest kernel](glossary/guest.md)，但 agent 仍能修改你開放寫入的 [host](glossary/host.md) [workspace](glossary/workspace.md)。這是 Kaan Yagci 在 [〈Wait, Docker Sandboxes Aren’t Containers?〉](https://x.com/yagcidev/article/2120166357060768143) 指出的差別：sandbox 隔離了執行環境，但不會隔離 agent 能存取的所有資源。

Docker Sandboxes 不需要在 [host 安裝 Docker Desktop 或 Docker Engine](https://docs.docker.com/ai/sandboxes/install/)。在 macOS 和 Windows 上，[Docker Desktop 把 Linux containers 放在 Linux VM 裡執行](https://docs.docker.com/desktop/features/vmm/)。這些 [containers](glossary/container.md) 仍共用這台 VM 的 [kernel](glossary/kernel.md)。[Docker Sandboxes](https://docs.docker.com/ai/sandboxes/security/isolation/#hypervisor-isolation) 則是每個 sandbox 一台 VM，不是每個 container 一台。

```mermaid
---
config:
  flowchart:
    rankSpacing: 16
    nodeSpacing: 12
---
flowchart TB
    accTitle: Shared versus separate Linux kernels
    accDescr: Two Docker Desktop containers share one Linux VM kernel. Two local Docker Sandboxes run in separate microVMs, each with its own kernel.
    subgraph Desktop["Docker Desktop VM"]
        Containers["Containers A and B"] --> Shared["Shared Linux kernel"]
    end
    subgraph First["Sandbox A microVM"]
        KA["Linux kernel A"]
    end
    subgraph Second["Sandbox B microVM"]
        KB["Linux kernel B"]
    end
    Desktop ~~~ First ~~~ Second
```

Agent 的 Docker 指令會送到 [sandbox 內的 Docker Engine](https://docs.docker.com/ai/sandboxes/security/isolation/#docker-engine-isolation)。它不必存取 host 的 Docker socket，就能建置映像檔和執行 containers。寫入檔案則走另一條路：如果 [mount](glossary/mount.md) 可寫，變更就會直接寫入 host 的專案資料夾。

```mermaid
---
config:
  flowchart:
    rankSpacing: 16
    nodeSpacing: 14
    wrappingWidth: 128
---
flowchart TB
    accTitle: Docker commands and workspace writes take different paths
    accDescr: The agent sends Docker commands to the engine inside the microVM. It can still write to a mounted host project. The usual Docker Engine is outside the sandbox and not on either path.
    subgraph VM["Sandbox microVM"]
        Agent["Agent"] -->|Docker commands| Engine["Private Docker Engine"]
    end
    Agent -->|Writes through mount| Project["Host project folder"]
    Project ~~~ Usual["Host Docker Engine"]
```

獨立的 Docker Engine 無法取代[網路 policy](practice/data-and-access/network-policy.md)。例如，如果 agent 的 [Docker context](https://docs.docker.com/engine/manage-resources/contexts/) 指向正式環境的 Docker Engine、網路允許連線，而且 agent 能通過身分驗證，它就仍然能連到正式環境。比對 sandbox 內外的 `docker context ls` 輸出只能檢查用戶端設定，不能證明正式環境的存取已被封鎖。

使用[本機 workspace](https://docs.docker.com/ai/sandboxes/security/isolation/#workspace-isolation) 時，如果沒有指定路徑，`sbx run` 會將目前目錄當成可寫的 workspace。移除 sandbox 不會復原對該目錄的變更。用 [`--clone`](https://docs.docker.com/ai/sandboxes/security/isolation/#clone-mode) 讓 agent 編輯獨立的副本，方便先審查再帶回變更。VM 仍能讀取原始 repository 中的檔案，包括 `.env` 等未被 Git 追蹤的檔案。如果 agent 不需要任何專案檔案，可建立不掛載 host workspace 的 sandbox。

#### 何時選用 Docker Sandboxes？ {#when-to-choose-docker-sandboxes}

當 agent 需要存取本機專案，又需要自己的 Docker Engine 時，適合選用本機 Docker Sandboxes。例如，讓 agent 修正後端 bug、建置 image、用 [Docker Compose](https://docs.docker.com/compose/) 啟動資料庫，再跑整合測試。這些 containers 在 sandbox VM 裡執行，不會使用你平常的 Docker 環境。

- **把 sandbox 嵌入自己的應用程式：** [Gondolin](https://github.com/earendil-works/gondolin#feature-highlights) 也提供 Linux microVM。若你想用 JavaScript 定義檔案存取和對外 HTTP 連線的 policy，而不是透過 `sbx` 啟動 coding agent，可考慮 Gondolin。
- **由服務按需啟動 sandboxes：** 比較 [E2B Runtime](https://github.com/e2b-dev/infra) 和 [Docker Sandboxes 雲端 API 與 SDK](https://docs.docker.com/ai/sandboxes-api/)。兩者都能由程式建立 sandbox。[Docker 雲端 sandboxes](https://docs.docker.com/ai/sandboxes/cloud/local-vs-cloud/) 不會掛載發出啟動指令的電腦上的資料夾。要讓工作在無人操作時執行，先確認逾時設定和到期後的處理方式。

### 哪些 workload 共用 guest kernel？ {#which-workloads-share-a-guest-kernel}

[Isolation unit](glossary/isolation-unit.md) 是共用同一個邊界實例的一組 workload。比較範例中的兩個 container（A 和 B）在各種實作中分別在哪裡執行。

```mermaid
---
config:
  flowchart:
    rankSpacing: 24
    nodeSpacing: 16
    wrappingWidth: 106
---
flowchart TB
    accTitle: Virtual machine boundaries in three container environments
    accDescr: Docker Sandboxes can run several containers in one sandbox VM, Apple container starts a VM for each container, and Kata can run several containers in one Kubernetes pod VM.
    subgraph Docker["Docker Sandboxes: one VM"]
        direction LR
        DA["Container A"] ~~~ DB["Container B"]
    end
    subgraph Apple["Apple container: two VMs"]
        direction LR
        AA["VM for A"] ~~~ AB["VM for B"]
    end
    subgraph Kata["Kata: one VM per pod"]
        direction LR
        KA["Container A"] ~~~ KB["Container B"]
    end
    Docker ~~~ Apple ~~~ Kata
```

在 Docker 和 Kata 的範例中，A 和 B 共用 guest kernel。在 Apple 的範例中，它們在不同的 VM 裡執行。如果兩個 workload 必須在 VM 邊界彼此隔離，就要確認 runtime 是否會把它們放在同一個 guest 裡。

## 不使用 guest Linux kernel 的 container 與 process {#containers-and-processes-without-a-guest-linux-kernel}

- [Google gVisor](https://gvisor.dev/docs/architecture_guide/intro/) 提供 OCI runtime `runsc`。其中的 **Sentry** 是 [user-space kernel](glossary/user-space-kernel.md)，負責處理 Linux [system calls](glossary/system-call.md)，這些呼叫來自 [workload](glossary/workload.md)。即使在 gVisor 的 KVM 平台上，Linux 系統介面仍由 Sentry 提供；Sentry 本身不是 Kata 那樣的獨立 Linux guest kernel。用實際的 workload 測試相容性與效能，不要假設每個 Linux 介面的行為都完全相同。
- [Anthropic Sandbox Runtime](https://github.com/anthropic-experimental/sandbox-runtime) 不需要 guest VM 就能限制原生 process。它在 Linux 上使用 [Bubblewrap](https://github.com/containers/bubblewrap)，在 macOS 上使用 Seatbelt，並透過 proxy 限制網路。這是 [operating-system process sandbox](glossary/operating-system-process-sandbox.md)：與 gVisor 不同，workload 仍直接使用 host 作業系統的 kernel，並受該作業系統的限制。

## Agent Substrate：在 Kubernetes 上為每個 Actor 建立獨立 sandbox {#agent-substrate}

[Agent Substrate](agent-substrate.md) 用一組預先啟動的 Kubernetes worker pods 執行 Actor。一個 pod 可以同時承載多個 Actor，每個 Actor 都有自己的 gVisor sandbox，或由 Cloud Hypervisor 提供虛擬機的 Kata Containers microVM。Substrate 把休眠的 Actor 存成 [snapshot](glossary/snapshot.md)，收到請求時再還原，不需要讓每個 Actor 都占用一個持續運作的 pod。

## Code Mode：隔離 tool script，而不是 shell {#code-mode-isolating-tool-scripts-instead-of-shells}

在 [Code Mode](glossary/code-mode.md) 中，模型會撰寫程式來呼叫 [tools](glossary/tool.md)，並整合它們的結果。外層應用程式決定哪些 tool 可用，以及各個 tool 可以做什麼。執行這個程式的 sandbox 不會自動限制 [host tool handlers](glossary/host-function.md) 或 agent 的其他部分。

比較各種實作之前，先看看一次 issue 查詢怎麼進行：

```mermaid
---
config:
  sequence:
    actorMargin: 12
    diagramMarginX: 8
    width: 78
    mirrorActors: false
---
sequenceDiagram
    accTitle: An issue lookup in Code Mode
    accDescr: The outer agent runs a generated script inside a sandbox. The script requests an issue title from a host tool outside the sandbox. The tool checks access and returns only the title.
    participant Agent as Agent
    box Script sandbox
        participant Script as Script
    end
    participant Tool as Host tool

    Agent->>Script: Run script
    Script->>Tool: Look up issue
    Note over Tool: Check access
    Tool-->>Script: Return title
    Script-->>Agent: Return summary
```

Host tool handler 會查驗呼叫者是否有權讀取 issue。Sandbox 限制 script 可以呼叫哪些 tool，但不會逐一對 tool 請求進行授權（[authorize](glossary/authorization.md)）。

| 實作 | 執行邊界 | 有什麼不同？ |
| --- | --- | --- |
| [Pi `codemode`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/README.md) | 編譯成 [Wasm](glossary/webassembly.md) 的 QuickJS（`quickjs-wasi`） | 此處檢視的 Pi 修訂版本會執行 JavaScript，並注入 tool 供 script 使用。Script 無法直接存取 Node API、檔案系統或網路。使用 `quickjs-wasi` 不代表 sandbox 允許存取通用的 [WASI](glossary/webassembly-system-interface.md) 檔案系統。 |
| [Earendil `djs`](https://github.com/earendil-works/djs/blob/c34b2a5974db47d9caafe7083a67ce4408d7333d/README.md) | 以 Rust 撰寫、主要以 Wasm 為目標的 JavaScript/TypeScript 引擎 | 設計目標是在受控輸入下進行確定性執行，並能暫停及恢復 script。專案將它描述為 QuickJS 的替代品，並隨附 Pi 轉接器。上面提到的 Pi 修訂版本仍[依賴 `quickjs-wasi`](https://github.com/earendil-works/pi/blob/9c4652688590abb836b40ebd1e4725ecf9a7c7d1/packages/codemode/package.json)；先確認已安裝的版本，不要直接假設它已完成遷移。 |
| [OpenCode Code Mode](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md) | 用於類 JavaScript script 的 [Restricted interpreter](glossary/restricted-interpreter.md)，不是 Wasm sandbox | 使用 [Psychoscript](https://github.com/anomalyco/psychoscript) 直譯受支援的 JavaScript 子集。host 可透過 tool 或 `fetch` 等 extension function 開放對外存取。 |
| [Cloudflare Dynamic Workers](https://blog.cloudflare.com/dynamic-workers/) | V8 [engine isolate](glossary/engine-isolate.md) | 在 Workers runtime 裡執行動態載入的程式碼。呼叫端可以封鎖對外請求，並傳入特定的繫結。[Cloudflare 的 Linux container sandbox](https://developers.cloudflare.com/sandbox/) 則是另一個選項：每個實例都是一台 microVM。 |
| [Wasmtime](https://docs.wasmtime.dev/security.html) | 通用 Wasm runtime | 適用於以 Wasm 模組而非任意 Linux 二進位檔散布的 workload。嵌入 Wasmtime 的應用程式控制可用的匯入項目和 host 能力。 |

如果 script 可使用不受限制的 `bash` tool 或寫入範圍很廣的 API，即使直譯器沒有直接的 I/O，它也不是低權限的。每次呼叫 tool 都要在 host 邊界進行授權。如果某個 tool 需要執行原生程式碼，可以把程式碼交給另一個 Linux sandbox 執行。

## 2026 年有哪些變化 {#what-is-changing-in-2026}

1. **環境佈建正從開機轉向還原。** [E2B Runtime](https://github.com/e2b-dev/infra) 從已開機的 Firecracker 範本還原，並支援暫停與恢復 sandbox。[Vercel Sandbox](https://vercel.com/docs/sandbox) 也使用 Firecracker，並提供 snapshots。[Amazon Bedrock AgentCore Runtime V2](https://aws.amazon.com/about-aws/whats-new/2026/11/new-agentcore-runtime-default/) 於 2026 年 11 月 12 日成為新 runtime 的預設版本，並從預先準備的 snapshot 還原 microVM session。區分 [cold boot](glossary/cold-boot.md) 和從 snapshot 還原。分別量測各種啟動方式要等多久才能執行第一個可用的命令。確認 snapshot 包含磁碟狀態、記憶體，還是兩者都有，以及其中是否可能含有憑證。
2. **Control plane 正逐漸與執行後端分開。** [Kubernetes Agent Sandbox](https://agent-sandbox.sigs.k8s.io/docs/) 增加了宣告式生命週期 API、範本、sandbox 領用申請和 [warm pools](glossary/warm-pool.md)。它可以使用 gVisor 或 Kata，但邊界由所選的 runtime 決定。[NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) 則示範了 policy 層：由 gateway 管理 sandbox 存取權，且只能向核准的對外目的地提供憑證。比較這些功能時，要與執行邊界分開評估。
3. **硬體輔助隔離不限於 host KVM。** 2026 年 11 月 9 日，[AWS 宣布推出適用於 EKS、ECS 和 EC2 的 Nitro Sandboxes](https://aws.amazon.com/about-aws/whats-new/2026/11/nitro-sandboxes-eks-ecs-ec2/)。設定為使用 Nitro Sandboxes 的 EKS pod 或 ECS task 各自取得一台由 Nitro 管理的 VM。在 EC2 上，Firecracker 無須使用上層執行個體中的 KVM 就能管理 guest。
4. **同一個 agent 可以使用不只一個邊界。** Cloudflare 的文件介紹了兩種做法：只需呼叫幾個方法的程式碼可在 isolate 中執行，需要完整環境的程式碼則在 Linux microVM 中執行。本機或自行架設的技術堆疊也可採用相同的分工：在 Wasm 或 restricted interpreter 中執行 tool script，只有需要時才將建置或測試交給 Linux sandbox。

## 如何評估候選方案 {#how-to-evaluate-a-candidate}

1. **選擇隔離單位。** 決定需要分開隔離的是 [sessions](glossary/sandbox-session.md)、[tenants](glossary/tenant.md)、pod，還是個別的 tool 呼叫。檢查清理是否確實執行，以及在重新啟動、從 snapshot 還原和建立分支副本時，哪些狀態會保留。
2. **列出會跨越邊界的項目。** 記錄每個 host mount、socket、網路路由、憑證，以及 tool API。不需要直接編輯時，優先選用唯讀 workspace 或 workspace 副本。限制對外流量；如果能由 policy 中介元件按請求提供憑證，就將可重複使用的憑證留在 sandbox 之外。
3. **檢查每一條必要的存取規則。** 使用無害的測試資料。證明允許的操作會成功，而禁止的操作會因規則而失敗，不是因為資源原本就不存在。本機範例請見[驗證存取規則](practice/verification/verifying-access-rules.md)。
4. **對每個符合要求的候選方案量測同一項工作。** 分別記錄到首次輸出及到完成所需的時間。如果排隊和結果傳輸會影響結果，就一併計入。報告資源使用量、相容性和快取狀態，不要假設兩種啟動方式所做的事相同。本機計時範例請見[量測 sandbox](practice/verification/measuring-a-sandbox.md)。

參考[選擇 sandbox](practice/design/choosing-a-sandbox.md)，將這份檢查清單用於設計決策。這兩項實作練習只檢查一種 Bubblewrap 設定，不能作為任何受調查產品或實際部署設定的驗證依據。
