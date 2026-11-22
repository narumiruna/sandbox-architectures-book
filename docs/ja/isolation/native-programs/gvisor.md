# gVisor

[gVisor](https://gvisor.dev/docs/architecture_guide/intro/) は、Linux [container](../../glossary/container.md) を実行する際に、別の Linux [guest kernel](../../glossary/guest.md) を起動しません。gVisor の [user-space kernel](../../glossary/user-space-kernel.md) である **Sentry** が、sandbox 内のプログラムからの要求を処理します。その代わり、互換性には制約があります。gVisor が Linux のインターフェースを独自に実装しているため、未対応の機能や動作が異なる機能があります。

## ファイルを開く要求はどこに届くか {#where-the-file-request-goes}

1. [Lamp](../../practice/design/from-issue-to-patch.md) のテストランナーは、`total.c` を開くために [system call](../../glossary/system-call.md) を発行します。Sentry は sandbox から見えるファイルシステム内でその呼び出しを処理し、プログラムの呼び出しを [host](../../glossary/host.md) の kernel に直接転送することはありません。
2. host のファイルを公開する設定では、gVisor は **Gofer** という補助 process を使い、[その mount へのアクセスを提供](https://gvisor.dev/docs/user_guide/filesystem/)できます。設定によっては、Gofer はファイル操作を一つずつ処理する代わりに、Sentry が公開されたファイルを直接操作できるようにします。基盤となるリソースについては、gVisor は引き続き host kernel に依存します。host のほかの部分を隠しても、明示的に sandbox に mount したファイルは隠れません。

## プラットフォームによって何が変わるか {#what-changes-with-the-platform}

gVisor の[プラットフォーム](https://gvisor.dev/docs/architecture_guide/platforms/)は、Sentry が呼び出しを捕捉し、プログラムの実行を管理するための仕組みです。**systrap** は CPU の仮想化支援を必要としません。**KVM** プラットフォームは[ハードウェア支援による仮想化](hardware-backed-virtual-machines.md)を使いますが、Linux のインターフェースを提供するのは引き続き Sentry です。KVM を使っても、gVisor は独自の Linux kernel を起動する [MicroVM](microvm.md) にはなりません。

## gVisor を選ぶ前に確認すること {#what-to-verify-before-choosing-gvisor}

- **Runtime:** gVisor は [OCI](../../glossary/open-container-initiative.md) の [container runtime](../../glossary/container-runtime.md) である `runsc` を提供します。ジョブの実行時に `runsc` が選ばれるように設定されているか確認してください。container image だけでは隔離境界は決まりません。
- **互換性:** [対応する Linux の機能](https://gvisor.dev/docs/user_guide/compatibility/)を確認してください。たとえば、gVisor では sandbox の中からネイティブのブロックデバイスを mount できません。セットアップからテストまで、ジョブ全体を実行してください。シェルが起動するだけでは、ビルドが成功するとは限りません。
- **共有:** 同じ gVisor sandbox 内のプログラムは Sentry を共有します。どのジョブが同じ sandbox を共有してよいかを決め、mount、ネットワークアクセス、credentials の[アクセスルールを検証してください](../../practice/verification/verifying-access-rules.md)。

選び方については、[MicroVM vs gVisor](microvm-vs-gvisor.md) を参照してください。
