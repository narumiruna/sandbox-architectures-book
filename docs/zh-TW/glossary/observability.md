# Observability

Observability 是指能根據系統留下的紀錄，了解它做過什麼。Sandbox 維運人員可以根據狀態變更、時間戳記或已遮蔽敏感資訊的日誌，找出工作在哪個環節失敗。

例如，未出現就緒事件且工作區逾時，表示問題可能出在環境配置階段。如果 worker 已就緒，之後才出現編譯器的診斷訊息，問題則可能出在建置階段。請分開記錄這些情況，避免將 policy 拒絕誤判為命令錯誤。

請參閱[可觀測性與除錯（英文）](../../practice/operations/observability-and-debugging.md)。
