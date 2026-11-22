# Resident set size (RSS)

Resident set size is the amount of a process's memory currently in physical memory. Peak RSS is the highest reported value over a measurement interval. It is not the amount of all memory the process has reserved.

A launcher can have a small peak RSS while several compiler processes use more memory together. Record which process or accounting boundary a measurement covers before comparing runs.

See [Measuring a sandbox](../practice/verification/measuring-a-sandbox.md).
