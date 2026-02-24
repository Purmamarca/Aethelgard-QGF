# Sentinel's Journal

## 2024-05-23 - Scientific Engine Resource Exhaustion
Vulnerability: `AethelgardEngine` and `AethelgardEngineGPU` allowed unbounded `grid_size` and `iterations` inputs, potentially leading to Memory Exhaustion (DoS) or CPU lockup.
Learning: Scientific computing libraries often assume trusted input and omit validation, but when exposed (e.g., via web visualizers), this becomes a DoS vector.
Prevention: Enforce strict upper bounds on all dimension-defining parameters (grid size, iterations) at the public API boundary (`__init__`, public methods).

## 2026-05-24 - Time Evolution Resource Control
Vulnerability: `AethelgardEngineTimeEvolution` lacked validation for `dt` and `time_steps`, allowing for potential resource exhaustion or physical instability (e.g., negative time steps).
Learning: When extending classes, ensure new parameters (`dt`, `time_steps`) also receive the same level of rigorous input validation as the parent class.
Prevention: Added strict type and range checks for `dt` (positive number) and `time_steps` (positive integer, max 10000) in `aethelgard_time_evolution.py`.
