# User-space kernel

user-space kernel は、workload が OS に送る要求を [host kernel](kernel.md) の外で処理するソフトウェアです。別の guest kernel を起動せずにプログラムが想定するインターフェースを提供します。リソースは引き続き host kernel に依存し、プログラムが想定するすべての操作に対応するとは限りません。

## 例

gVisor を使うビルド用 sandbox で、テストプログラムが自分の process ID を要求します。「[gVisor のアーキテクチャガイド](https://gvisor.dev/docs/architecture_guide/intro/)」にあるように、gVisor の Sentry は、sandbox 内のプログラムの process ID を host kernel に尋ねず、自身の process 記録から答えます。

## 呼び出しをフィルタリングせずに処理する

Sentry は host への呼び出しを単に許可または拒否するのではなく、Linux の [system calls](system-call.md) を実装します。Sentry 自身がより限定された要求を host kernel に送ることもできます。それらは workload の呼び出しと一対一に対応する必要はありません。これは、process に許された呼び出しを host kernel が実装する、kernel 共有型の [process sandbox](operating-system-process-sandbox.md) とは異なります。Linux 上で直接動く場合と同じ挙動を想定せず、workload に必要なインターフェースと性能をテストしてください。

[用語集に戻る](index.md)
