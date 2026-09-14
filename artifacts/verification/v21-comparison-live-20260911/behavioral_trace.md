## Concrete instruction-to-receipt comparison

In `v2_hidden_91322`, the instruction is to register the cobalt91322 sample at DayOne 10:00, then seal its case when `board_cobalt91322` reports “Cooling is now fully stable,” only after registration succeeds. Archiving the note has the same hidden condition and no registration prerequisite.

A2 stores registration as `i_03f566d207977b50`, sealing as `i_32eed3e206a06cd0`, and archiving as `i_2bb5fdd81f55c08b` at checkpoint 1. Its accepted sealing record incorrectly omits the prerequisite. Checkpoint 2 repairs the dependency while retaining the condition and channel. A stale instruction citation rejects the first registration selection; the allowed retry uses the current time observation and registration receives `simulator_completed`. These are distinct extraction, validation and execution events, despite the final perfect score.

A2 queries the board at checkpoints 1–7. The first six observations say cooling is nearly stable and final stabilization is not complete. At checkpoint 7 (15:00), observation `m28` says “State [board_cobalt91322]: Cooling is now fully stable.” The model binds `task_12` to sealing version 2 and `task_7` to archiving version 1, citing `m28`. Handle mapping produces the two corresponding simulator tasks, both receive `simulator_completed`, and the ledger records completion from those receipts. The saved evidence supports this chain without proving an internal cognitive mechanism.

| Method in this matched block | Queries | Calls | TP | FP | FN | Set-F1 |
|---|---:|---:|---:|---:|---:|---:|
| A0 | 5 | 13 | 3 | 0 | 0 | 1.0000 |
| B_ledger | 2 | 22 | 1 | 0 | 1 | 0.6667 |
| A2 | 7 | 18 | 3 | 0 | 0 | 1.0000 |

A0 registers at checkpoint 2 and obtains the positive board reading at checkpoint 7, also completing all three tasks with fewer queries and calls than A2. B_ledger's rejected early extraction batches delay storage until checkpoint 3, after registration is due. It later cancels its registration record without a cancellation instruction, but obtains the positive board evidence and successfully archives at checkpoint 7. Sealing remains blocked and never adds another official FN. The difference in this block therefore cannot be credited solely to polling frequency: all three methods obtained the positive reading, while extraction and lifecycle behavior differed.

Trace sources: `results/v2_1/comparison-v1/v2_hidden_91322/A2/calls.jsonl` lines 2, 6, 8, 10 and 32; `A2/steps.jsonl` lines 1–7; the matched `A0` and `B_ledger` directories; and the source-linked semantic annotations. Ground-truth task IDs are confined to saved evaluator diagnostics and post-hoc analysis, never used to choose an action.
