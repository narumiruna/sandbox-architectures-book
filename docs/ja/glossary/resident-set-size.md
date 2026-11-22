# Resident set size (RSS)

resident set size は、process が使うメモリのうち、現在物理メモリに載っている量です。peak RSS は、測定期間中に報告された最大値です。process が予約したメモリ全体の量ではありません。

起動プログラムの peak RSS が小さくても、複数のコンパイラ process が合わせてより多くのメモリを使うことがあります。実行結果を比較する前に、どの process または集計範囲を測定したかを記録してください。

「[sandbox の測定](../practice/verification/measuring-a-sandbox.md)」を参照してください。
