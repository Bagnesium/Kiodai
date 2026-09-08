# Failure Taxonomy

This taxonomy is preregistered as a coding frame. Counts must come from trajectories, not intuition.

| Code | Root cause | Required evidence |
|---|---|---|
| EXTRACT | Intention extraction | Instruction observed but no usable representation retained |
| TRIGGER-PARSE | Trigger parsing | Wrong cue/time/channel interpretation |
| TEMPORAL | Temporal reasoning | Incorrect time, window, recurrence, or delay judgment |
| EVENT-MATCH | Event matching | Observed event incorrectly matched or missed |
| MONITOR-MISS | Missing monitoring | Relevant channel not queried in a useful interval |
| MONITOR-EXCESS | Excessive monitoring | Queries add cost without relevant evidence |
| VERSION-STALE | Stale version | Superseded instruction executed or retained |
| UPDATE | Update application | Override/reschedule applied incorrectly |
| CANCEL | Cancellation handling | Canceled task executed or cancellation cascaded incorrectly |
| DEPENDENCY | Dependency tracking | Child executed early or never armed after parent completion |
| PREMATURE | Premature execution | Correct task before valid trigger/window |
| DUPLICATE | Duplicate execution | Completed task executed again |
| CONTEXT | Context loss | Intention disappears after delay, truncation, or restart |
| REASONING | Model reasoning | Necessary evidence present but decision remains unsupported |
| TOOL | Tool failure | Query/action infrastructure prevents correct behavior |
| FORMAT | Output-format failure | Response cannot be parsed or violates action protocol |
| EVALUATOR | Evaluator mismatch | Claimed behavior and scoring semantics disagree |
| AMBIGUOUS | Benchmark ambiguity | Multiple interpretations remain reasonable after review |

Each coded failure must link to the raw call, visible observation, active intention/version if applicable, model action, and official scoring consequence.

