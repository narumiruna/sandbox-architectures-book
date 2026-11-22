# Resource limit

Resource limit 為工作可使用的資源設定上限，例如記憶體、磁碟空間、CPU 時間或同時執行的 worker 數量。它不決定工作可以存取哪些檔案或服務。

例如，磁碟用量上限可以避免 agent 的建置工作用完儲存空間，卻不能阻止建置工作讀取誤開放的目錄中的資料。請另外使用 [policy](policy.md) 控制存取。

請參閱[資源限制（英文）](../../practice/operations/resource-limits.md)。
