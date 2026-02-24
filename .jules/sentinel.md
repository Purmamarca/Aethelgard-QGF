# Sentinel's Journal

## 2024-05-23 - Scientific Engine Resource Exhaustion
Vulnerability: `AethelgardEngine` and `AethelgardEngineGPU` allowed unbounded `grid_size` and `iterations` inputs, potentially leading to Memory Exhaustion (DoS) or CPU lockup.
Learning: Scientific computing libraries often assume trusted input and omit validation, but when exposed (e.g., via web visualizers), this becomes a DoS vector.
Prevention: Enforce strict upper bounds on all dimension-defining parameters (grid size, iterations) at the public API boundary (`__init__`, public methods).
