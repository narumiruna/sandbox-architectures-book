# Snapshot

snapshot は、後でシステムが復元できるよう保存した状態です。ディスクのみの snapshot はストレージを保存しますが、実行中のプログラムは保存しません。メモリを含む snapshot は、必要なプロセッサとデバイスの状態も含めれば、実行中の状態を保存できます。保存メモリには [credentials](credential.md) などの秘密情報が含まれ得るため、機密データとして扱ってください。

## 例

テストサービスは Linux sandbox を起動し、ユーザーに割り当てる前にテンプレートを保存します。ディスクのみの snapshot なら準備済みファイルを再利用できますが、Linux を起動し、そのサービスを開始する必要があります。実行中の VM の snapshot なら、保存時点からサービスを再開できます。いずれも新しい session 用にユーザーの workspace とアクセス権を設定する必要があります。

## 復元できるもの

snapshot が実際に保存するファイルと外部リソースを確認してください。たとえば [Firecracker v1.11.0](https://github.com/firecracker-microvm/firecracker/blob/v1.11.0/docs/snapshotting/snapshot-support.md#overview) は guest メモリと VM の状態を別々のファイルに保存します。対応するディスクは運用者が管理し、既存のネットワーク接続が維持される保証はありません。復元先の互換性と対応するディスク状態を確認してください。

一つのメモリ snapshot から複数の VM を再開すると、一意であるはずの識別子などを引き継ぐことがあります。2021 年のプレプリント「[Restoring Uniqueness in MicroVM Snapshots](https://arxiv.org/abs/2102.12892)」は、復元インスタンスごとに新しい状態が必要な理由を説明しています。共有テンプレートにユーザー固有のデータや秘密情報を含めないでください。ディスクの snapshot にもファイルに書かれた秘密情報が入る場合があります。

snapshot は保存済みの artifact であり、準備済み sandbox の [warm pool](warm-pool.md) ではありません。サービスは snapshot でプールを補充したり、[cold start](cold-start.md) が必要なときに snapshot を復元したりできます。

[用語集に戻る](../glossary.md)
