# Open Container Initiative (OCI)

[Open Container Initiative](https://opencontainers.org/) は、container のパッケージ化、配布、実行に関する公開仕様を維持しています。OCI 互換性があれば、異なる tool を組み合わせて使いやすくなります。ただし、実行中のプログラムを host から何が分離するかは、OCI 互換性だけでは分かりません。

## 例

あるビルドサービスは、コンパイラーとテストツールを OCI [container image](container-image.md) としてパッケージ化します。共有の host kernel を使う方式と [virtual machine](virtual-machine.md) を使う方式の両方がその image と内蔵プログラムに対応していれば、どちらの方式でも同じ image からテスト用 sandbox を起動できます。

## 各仕様が定める範囲

[Image Specification v1.1.0](https://github.com/opencontainers/image-spec/tree/v1.1.0) は、ファイルシステムへの変更と設定をまとめるパッケージを定義します。[Distribution Specification v1.1.0](https://github.com/opencontainers/distribution-spec/tree/v1.1.0) は、container image を保管するサービスである registry と tool の間で、コンテンツを送受信する方法を定義します。[Runtime Specification v1.2.1](https://github.com/opencontainers/runtime-spec/tree/v1.2.1) は、準備済みの container を実行する際の設定とライフサイクルを定義します。コードが何にアクセスできるかを知るには、選んだ [container runtime](container-runtime.md) とその設定を確認してください。

[用語集に戻る](index.md)
