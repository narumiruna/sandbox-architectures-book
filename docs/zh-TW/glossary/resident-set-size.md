# Resident set size (RSS)

Resident set size 是 process 目前存放在實體記憶體中的記憶體用量。峰值 RSS 是量測期間回報的最高值，並不等於該 process 保留的全部記憶體。

啟動程式的峰值 RSS 可能很低，但它啟動的多個編譯器 process 合計可能用掉更多記憶體。比較各次執行前，請記錄量測涵蓋哪個 process 或哪個用量統計範圍。

請參閱[量測 sandbox（英文）](../../practice/verification/measuring-a-sandbox.md)。
