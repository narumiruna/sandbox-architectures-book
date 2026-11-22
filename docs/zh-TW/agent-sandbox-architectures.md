# Agent 的 sandbox 架構 {#agent-sandbox-architectures}

*本調查更新於 2026 年 11 月 22 日。本章比較的是文件所描述的架構，不是實測效能，也不是安全保證。*

本調查比較不同專案如何隔離協助開發的 [agents](glossary/agent.md) 和它們產生的程式碼。

## 執行邊界 {#execution-boundaries}

[Isolation boundary](glossary/isolation-boundary.md) 限制程式可以觸及的範圍。[Policy](glossary/policy.md) 規定哪些項目應可跨越這個邊界。若要瞭解六種隔離方式，請先閱讀 [Sandbox 的隔離邊界](sandbox-isolation-boundaries.md)。

[Virtual machine monitor (VMM)](glossary/virtual-machine-monitor.md) 管理 [virtual machine (VM)](glossary/virtual-machine.md) 和 VM 可見的裝置。VMM 並不是完整的 [sandbox](glossary/sandbox.md) 產品：可由獨立的 [control plane](glossary/control-plane.md) 決定何時啟動 VM，以及要提供哪些資源給它。

## 使用硬體輔助的 Linux 環境 {#hardware-backed-linux-environments}

| 專案 | 提供的功能 | 邊界與範圍 |
| --- | --- | --- |
| [Docker Sandboxes (`sbx`)](https://docs.docker.com/ai/sandboxes/architecture/) | 可直接使用的開發 agent 環境 | 每個本機 sandbox 都在一台 [microVM](glossary/microvm.md) 裡執行，並有自己的 Docker daemon。即使無法存取 [host](glossary/host.md) 上的 Docker socket，agent 仍可建置和執行 [containers](glossary/container.md)。Host 的 [workspace](glossary/workspace.md) [mounts](glossary/mount.md) 和對外 proxy 各自涉及不同的信任決策。[本機安裝](https://docs.docker.com/ai/sandboxes/install/)說明 macOS、Windows 和 Linux 的需求。 |
| [libkrun](https://github.com/containers/libkrun) | 可嵌入的 VMM 函式庫，提供 Rust 和 C API | 在 Linux 上使用 [KVM](glossary/kernel-based-virtual-machine.md)，在 Apple silicon 上使用 [Hypervisor Framework](https://developer.apple.com/documentation/hypervisor)。呼叫端決定開放哪些 host 檔案和裝置。[Gondolin](https://github.com/earendil-works/gondolin/blob/main/docs/backends.md) 是一層 sandbox，可用 libkrun 或 QEMU 作為 VMM。 |
| [Cloud Hypervisor](https://github.com/cloud-hypervisor/cloud-hypervisor) | 通用的雲端 VMM | 在 KVM 或 [MSHV](glossary/microsoft-hypervisor.md) 上執行，支援 Linux 和 Windows [guests](glossary/guest.md)。它是後端，不是具有 workspace 和 [credential](glossary/credential.md) policy 的完整 agent sandbox。 |
| [Firecracker](https://github.com/firecracker-microvm/firecracker) | 供 microVM 使用的精簡 VMM | 一般部署是在 Linux 上使用 KVM。上游專案也記載了 [AWS Nitro Sandboxes 後端](https://github.com/firecracker-microvm/firecracker/tree/main/docs/nitro-sandboxes)，這個後端使用 AWS Nitro，而不是 host KVM。 |
| [Kata Containers](https://github.com/kata-containers/kata-containers/blob/main/docs/design/architecture/README.md) | 以 VM 為基礎的 [container runtime](glossary/container-runtime.md) | 在 [Kubernetes](https://kubernetes.io/docs/concepts/overview/) 中，[pod](glossary/pod.md) 在 guest VM 裡執行；同一個 pod 裡的 container 可以共用 guest [kernel](glossary/kernel.md)。Kata [支援多種 VMM](https://github.com/kata-containers/kata-containers/blob/main/docs/hypervisors.md)，包括 QEMU、Cloud Hypervisor 和 Firecracker。Kata 和 Firecracker 屬於不同層，不能直接互相替代。 |
| [Microsoft NVX](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/README.md) | 以 OpenVMM 為基礎的 microVM 技術堆疊和 guest runtime | 文件涵蓋使用 KVM 或 MSHV 的 Linux host，以及使用 [Windows Hypervisor Platform](glossary/windows-hypervisor-platform.md) 的 Windows host。Guest runtime 的設計目標是[每台 Linux microVM 執行一個 workload sandbox](https://github.com/microsoft/nvx/blob/42f413d226290e31ea288686d6f3dbfd20c45733/doc/design/4-guest-runtime-architecture.md)。 |
| [Apple `container`](https://github.com/apple/container/blob/main/docs/technical-overview.md) | Apple silicon 上的本機 [OCI](glossary/open-container-initiative.md) container 工具 | 透過 Apple 的 [Virtualization framework](https://developer.apple.com/documentation/virtualization)，**每個 container** 各執行一台輕量的 Linux VM。它以 [container images](glossary/container-image.md) 為輸入，但隔離邊界是 VM，而不是 user-space kernel。 |

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
| [OpenCode Code Mode](https://github.com/anomalyco/opencode/blob/5310e42203af41c3452ee44b24fc7d0c52aaa3cc/packages/codemode/README.md) | 用於類 JavaScript script 的 [Restricted interpreter](glossary/restricted-interpreter.md)，不是 Wasm sandbox | 使用 [Psychoscript](https://github.com/anomalyco/psychoscript) 直譯受支援的 JavaScript 子集。要存取檔案、網路和 API，須透過 host 提供的 tool。 |
| [Cloudflare Dynamic Workers](https://blog.cloudflare.com/dynamic-workers/) | V8 [engine isolate](glossary/engine-isolate.md) | 在 Workers runtime 裡執行動態載入的程式碼。呼叫端可以封鎖對外請求，並傳入特定的繫結。[Cloudflare 的 Linux container sandbox](https://developers.cloudflare.com/sandbox/) 則是另一個選項：每個實例都是一台 microVM。 |
| [Wasmtime](https://docs.wasmtime.dev/security.html) | 通用 Wasm runtime | 適用於以 Wasm 模組而非任意 Linux 二進位檔散布的 workload。嵌入 Wasmtime 的應用程式控制可用的匯入項目和 host 能力。 |

如果 script 可使用不受限制的 `bash` tool 或寫入範圍很廣的 API，即使直譯器沒有直接的 I/O，它也不是低權限的。每次呼叫 tool 都要在 host 邊界進行授權。如果某個 tool 需要執行原生程式碼，可以把程式碼交給另一個 Linux sandbox 執行。

## 2026 年有哪些變化 {#what-is-changing-in-2026}

1. **環境佈建正從開機轉向還原。** [E2B Runtime](https://github.com/e2b-dev/infra) 從已開機的 Firecracker 範本還原，並支援暫停與恢復 sandbox。[Vercel Sandbox](https://vercel.com/docs/sandbox) 也使用 Firecracker，並提供 [snapshots](glossary/snapshot.md)。[Amazon Bedrock AgentCore Runtime V2](https://aws.amazon.com/about-aws/whats-new/2026/11/new-agentcore-runtime-default/) 於 2026 年 11 月 12 日成為新 runtime 的預設版本，並從預先準備的 snapshot 還原 microVM session。區分 [cold boot](glossary/cold-boot.md) 和從 snapshot 還原。分別量測各種啟動方式要等多久才能執行第一個可用的命令。確認 snapshot 包含磁碟狀態、記憶體，還是兩者都有，以及其中是否可能含有憑證。
2. **Control plane 正逐漸與執行後端分開。** [Kubernetes Agent Sandbox](https://agent-sandbox.sigs.k8s.io/docs/) 增加了宣告式生命週期 API、範本、sandbox 領用申請和 [warm pools](glossary/warm-pool.md)。它可以使用 gVisor 或 Kata，但邊界由所選的 runtime 決定。[NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) 則示範了 policy 層：由 gateway 管理 sandbox 存取權，且只能向核准的對外目的地提供憑證。比較這些功能時，要與執行邊界分開評估。
3. **硬體輔助隔離不限於 host KVM。** 2026 年 11 月 9 日，[AWS 宣布推出適用於 EKS、ECS 和 EC2 的 Nitro Sandboxes](https://aws.amazon.com/about-aws/whats-new/2026/11/nitro-sandboxes-eks-ecs-ec2/)。設定為使用 Nitro Sandboxes 的 EKS pod 或 ECS task 各自取得一台由 Nitro 管理的 VM。在 EC2 上，Firecracker 無須使用上層執行個體中的 KVM 就能管理 guest。
4. **同一個 agent 可以使用不只一個邊界。** Cloudflare 的文件介紹了兩種做法：只需呼叫幾個方法的程式碼可在 isolate 中執行，需要完整環境的程式碼則在 Linux microVM 中執行。本機或自行架設的技術堆疊也可採用相同的分工：在 Wasm 或 restricted interpreter 中執行 tool script，只有需要時才將建置或測試交給 Linux sandbox。

## 如何評估候選方案 {#how-to-evaluate-a-candidate}

1. **選擇隔離單位。** 決定需要分開隔離的是 [sessions](glossary/sandbox-session.md)、[tenants](glossary/tenant.md)、pod，還是個別的 tool 呼叫。檢查清理是否確實執行，以及在重新啟動、從 snapshot 還原和建立分支副本時，哪些狀態會保留。
2. **列出會跨越邊界的項目。** 記錄每個 host mount、socket、網路路由、憑證，以及 tool API。不需要直接編輯時，優先選用唯讀 workspace 或 workspace 副本。限制對外流量；如果能由 policy 中介元件按請求提供憑證，就將可重複使用的憑證留在 sandbox 之外。
3. **檢查每一條必要的存取規則。** 使用無害的測試資料。證明允許的操作會成功，而禁止的操作會因規則而失敗，不是因為資源原本就不存在。本機範例請見[驗證存取規則](practice/verification/verifying-access-rules.md)。
4. **對每個符合要求的候選方案量測同一項工作。** 分別記錄到首次輸出及到完成所需的時間。如果排隊和結果傳輸會影響結果，就一併計入。報告資源使用量、相容性和快取狀態，不要假設兩種啟動方式所做的事相同。本機計時範例請見[量測 sandbox](practice/verification/measuring-a-sandbox.md)。

參考[選擇 sandbox](practice/design/choosing-a-sandbox.md)，將這份檢查清單用於設計決策。這兩項實作練習只檢查一種 Bubblewrap 設定，不能作為任何受調查產品或實際部署設定的驗證依據。
