# OS の process sandbox {#operating-system-process-sandboxes}

[operating-system process sandbox](../../glossary/operating-system-process-sandbox.md) を使うと、[agent](../../glossary/agent.md) は [host](../../glossary/host.md) 上のネイティブコマンドを、そのコマンドがアクセスできる範囲を制限した状態で使えます。sandbox の中に別の OS はありません。

## 要求を処理するのは誰ですか？ {#who-handles-the-request}

[Lamp](../../practice/design/from-issue-to-patch.md) のテストランナーが `total.c` を開こうとすると、その [process](../../glossary/process.md) は [system call](../../glossary/system-call.md) を発行し、host の [kernel](../../glossary/kernel.md) がその要求を処理します。Linux では、[mount namespace](../../glossary/namespace.md) によって、プロジェクトは含むが host の非公開ディレクトリは含まないファイルの見え方を、その process に与えることができます。[seccomp](../../glossary/seccomp.md) フィルターは、指定した種類の system call をブロックできますが、それだけではファイルパスごとのルールを強制できません。

たとえば、[リビジョン `0bbebed0` の Anthropic Sandbox Runtime](https://github.com/anthropic-experimental/sandbox-runtime/blob/0bbebed0aa9a8e628dc4df8bc30293550a1988eb/README.md) は、Linux では [Bubblewrap](https://github.com/containers/bubblewrap) を、macOS では Seatbelt プロファイルを使います。また、ネットワークプロキシを使って接続先が許可されているかを確認します。仕組みは host のプラットフォームによって異なるため、agent を実行するプラットフォームで動作を確認してください。

## 何が共有されますか？ {#what-stays-shared}

sandbox の内外の process は、同じ host kernel を使います。kernel は sandbox ごとに見えるファイルを変えられますが、host のディレクトリを読み書き可能な [mount](../../glossary/mount.md) として公開すると、プログラムはそのディレクトリにあるファイルを変更できます。

## 適した場面 {#when-to-use-it}

ローカルの agent に現在の OS のネイティブツールが必要で、host への無制限のアクセスは引き継がせたくないときは、この境界を選びます。たとえば、開発者がすでに利用しているコマンドラインツールを使うテストランナーに適しています。

## この境界では制限できないこと {#what-the-boundary-does-not-cover}

ファイルを見えなくしても、process にすでに渡した [credentials](../../glossary/credential.md) は取り除けません。また、ファイルのルールではネットワークを制限できません。引き継がれる環境変数と、開いたままの接続を確認してください。無害なファイルを使った確認と、それとは別のネットワークの確認で[アクセスルールを検証](../../practice/verification/verifying-access-rules.md)してください。さらに、パッケージマネージャーが起動したテストランナーなどの子 process を経由して、ファイルの確認を繰り返してください。
