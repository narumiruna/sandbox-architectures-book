# Engine isolate

Engine isolate は、JavaScript などの言語で書かれたコードを実行するソフトウェアである言語エンジン内の、独立した実行環境です。各 Isolate は、そこでスクリプトが作成するオブジェクトなど、独自の状態を持ちます。複数の Isolate が一つのオペレーティングシステムの Process を共有できるため、Isolate は別個の Process や [virtual machine](virtual-machine.md) ではありません。

## 例

Issue 管理システムが、二つのチームのスクリプトを別々の Isolate で実行します。一方のスクリプトは、他方から見えないように Issue のタイトル一覧をメモリーに保持できます。各スクリプトはタイトルを取得するために [host function](host-function.md) を呼び出し、その関数はスクリプトがどのプロジェクトの読み取りを許されているかを確認します。

## エンジンの状態と Host へのアクセス

[V8 13.8.258 Isolate API](https://github.com/v8/v8/blob/13.8.258/include/v8-isolate.h#L277-L285) は状態を分離するよう規定しています。一つの Isolate の V8 オブジェクトを別の Isolate で使ってはいけません。その分離を管理するのはエンジンです。エンジンを組み込むアプリケーションである [host](host.md) が、スクリプトから呼び出せる操作を決めます。[Cloudflare の Dynamic Workers のアーキテクチャ](https://blog.cloudflare.com/dynamic-workers/)はこの違いを示す例です。呼び出し元は、選んだサービスに名前を付けてスクリプトにアクセスを許可し、外部への直接要求を遮断できます。

Isolate は、Host function がスクリプトに代わって行うことを制限しません。公開する操作を一つずつスクリプトの権限と照合し、プラットフォームが CPU とメモリーの使用量をどう制限するかも確認します。ネイティブプログラムの実行が必要なタスクには、[operating-system process sandbox](operating-system-process-sandbox.md) など、それに対応する別の環境を使います。

[用語集に戻る](../glossary.md)
