# Warm pool

Warm pool 是一組在請求到來之前就準備好的 [sandboxes](sandbox.md)。請求可以直接領用其中一個，不必等待所有設定完成。預先完成的工作因平台而異；即使 sandbox 已經準備好，仍可能需要依請求個別設定。

## 範例

建置服務保留三個尚未分配的 Linux sandbox，其中已安裝編譯器，且命令服務正在執行。請求領用其中一個，掛接專案檔案並開始建置。如果三個都已被領用，下一個請求可能需要等待或進行 [cold start](cold-start.md)。

## 準備好的是實例，不是儲存的檔案

[control plane](control-plane.md) 會準備實例、將它們分配給各個請求，並可補充 pool。例如，[Kubernetes Agent Sandbox v1.0.12](https://github.com/kubernetes-sigs/agent-sandbox/blob/v1.0.12/examples/warmpool-quickstart/README.md) 說明如何用 `SandboxWarmPool` 準備實例，以及用 `SandboxClaim` 領用一個實例。這個生命週期機制不決定 sandbox 如何隔離 workload。

[snapshot](snapshot.md) 是已儲存的狀態。服務可以用還原 snapshot 的方式補充 warm pool，但如果只保留 snapshot，請求到來時仍須執行還原。Pool 提早完成工作，代價是在實例等待期間占用資源。請勿在尚未分配的實例中放入 [tenant](tenant.md) 資料，並在量測就緒時間時納入分配和 workspace 設定所需的時間。

[返回詞彙表](../glossary.md)
