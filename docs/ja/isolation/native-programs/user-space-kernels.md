# User-space kernel {#user-space-kernels}

[user-space kernel](../../glossary/user-space-kernel.md) を使うと、[agent](../../glossary/agent.md) は別の Linux [guest](../../glossary/guest.md) を起動せずに Linux プログラムを実行できます。この仕組みはプログラムが使う Linux のインターフェースを実装するため、プログラムからの要求は [host](../../glossary/host.md) の [kernel](../../glossary/kernel.md) に直接届きません。

## 要求を処理するのは誰ですか？ {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md) のテストランナーが `total.c` を開くために [system call](../../glossary/system-call.md) を実行すると、[gVisor](https://gvisor.dev/docs/architecture_guide/intro/) 内では **Sentry** がその要求を処理します。Sentry はテストランナーから見えるファイルシステム内で、そのパスが指すファイルを探します。gVisor はデータを取得するために、host に対して独自の、範囲を絞った要求を出すことができます。実行中のプログラムの system call をそのまま転送するわけではありません。

## 何が共有されますか？ {#what-stays-shared}

同じ gVisor sandbox 内のプログラムは Sentry を共有します。gVisor は、基盤となるリソースについては引き続き host kernel に依存します。一方、[VM](../../glossary/virtual-machine.md) は guest kernel を起動します。[process sandbox](operating-system-process-sandboxes.md) では、プログラム自身が host kernel に system call を発行します。

## 適した場面 {#when-to-use-it}

Linux [containers](../../glossary/container.md) を実行する必要があり、実行する処理と host kernel の間に別の層を置きたいときは、この境界を選びます。Linux のインターフェースを再実装しているため、プログラムが依存する動作の中には、[gVisor では未対応のものや、動作が異なるもの](https://gvisor.dev/docs/user_guide/compatibility/)があります。コマンドが起動するかだけでなく、実際のインストール、ビルド、テストの手順を確認してください。

## この境界では制限できないこと {#what-the-boundary-does-not-cover}

Sentry は、与えられた範囲のファイルシステムを提供します。Lamp のどのデータを agent が読み取ってよいかを決めるのは Sentry ではありません。[runtime](../../glossary/runtime.md) が、意図した [workspace](../../glossary/workspace.md) とネットワークアクセスだけを提供していることを確認してください。
