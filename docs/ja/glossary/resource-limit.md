# Resource limit

resource limit は、ジョブが使用できるメモリ、ディスク容量、CPU 時間、同時に動く worker の数などに上限を設けます。ジョブがどのファイルやサービスにアクセスできるかは決めません。

たとえば、ディスク容量の上限を設ければ、agent のビルドでストレージを使い切るのを防げます。ただし、誤って公開されたディレクトリからビルドがデータを読み取るのは防げません。アクセスは [policy](policy.md) で別に制御してください。

「[resource limit（英語）](../../practice/operations/resource-limits.md)」を参照してください。
