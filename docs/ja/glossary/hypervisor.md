# Hypervisor

Hypervisor は、[virtual machine](virtual-machine.md) が物理コンピューターのプロセッサーとメモリーをどのように使うかを制御するソフトウェアです。プロジェクトによっては *hypervisor* と *virtual machine monitor* を同じ意味で使います。本書では、VM とその仮想デバイスを管理するコンポーネントを [virtual machine monitor (VMM)](virtual-machine-monitor.md) と呼びます。

## 例

あるサーバーが、2 つのテスト用 sandbox を別々の VM で実行します。それぞれの VM には、自分専用の仮想プロセッサーとメモリーが見えます。Hypervisor によって、どちらの guest も相手のメモリーに直接アクセスすることなく、同じ物理マシンを利用できます。

## 仮想環境での実行とアクセス policy

ハードウェア支援を使う hypervisor は、プロセッサーの機能で guest の命令を実行し、guest がアクセスできる物理メモリーを制限します。VMM は [KVM](kernel-based-virtual-machine.md) などの host インターフェースを使ってこの実行環境を設定し、guest のプログラムが必要とするデバイスの動作を提供できます。これらの役割を公開する方法の違いは、[Linux KVM API](https://docs.kernel.org/virt/kvm/api.html) と [Microsoft Hypervisor の仕様](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/tlfs) を比較すると分かります。

Sandbox にプロジェクトディレクトリを見せるか、外部サービスへの接続を許すかは、hypervisor が決めることではありません。何を公開し、[policy](policy.md) をどう適用するかは、周囲のシステムに依存します。

[用語集に戻る](../glossary.md)
