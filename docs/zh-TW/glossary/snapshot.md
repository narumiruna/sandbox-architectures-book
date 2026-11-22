# Snapshot

Snapshot 是系統日後可以還原的已儲存狀態。只有磁碟的 snapshot 會保留儲存內容，但不會保留執行中的程式。含有記憶體的 snapshot 若也包含必要的處理器和裝置狀態，就能保留執行狀態。儲存的記憶體可能包含 [credentials](credential.md) 和其他機密，因此應視為敏感資料。

## 範例

測試服務啟動 Linux sandbox，並在分配給使用者之前儲存範本。若使用只有磁碟的 snapshot，服務可以重用準備好的檔案，但必須開機並啟動 Linux 服務。若使用執行中 VM 的 snapshot，則可以從儲存時的狀態繼續執行這些服務。無論哪種方式，服務仍須為新 session 設定使用者的 workspace 和存取權限。

## 還原能恢復什麼

請確認 snapshot 實際保留了哪些檔案和外部資源。例如，[Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/snapshotting/snapshot-support.md#overview) 將 guest 記憶體和 VM 狀態分別寫入不同檔案。底層磁碟由維運人員管理，既有的網路連線不一定能保留。請確認還原環境相容，而且有相符的磁碟狀態。

多個 VM 從同一份記憶體 snapshot 恢復執行時，可能會繼承原本應該唯一的識別碼或其他值。2021 年的預印本 [Restoring Uniqueness in MicroVM Snapshots](https://arxiv.org/abs/2102.12892) 解釋為什麼還原的實例需要各自取得新的狀態。請勿在共用範本中放入使用者專屬資料或機密。磁碟 snapshot 也可能包含寫入檔案的機密。

Snapshot 是已儲存的 artifact，不是由預先準備好的 sandbox 組成的 [warm pool](warm-pool.md)。服務可以使用 snapshot 補充 pool，也可以在需要 [cold start](cold-start.md) 時還原一份 snapshot。

[返回詞彙表](../glossary.md)
