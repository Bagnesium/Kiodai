# Related Work

## PM-Bench

Liu and Gabriel, “PM-Bench: Evaluating Prospective Memory in LLM Agents,” arXiv:2607.12385 / COLM 2026. The released repository reports an optional-heartbeat macro Set-F1 of 65.1% across eight model backbones. The best individual released result must be kept distinct from that macro aggregate.

Primary record: <https://arxiv.org/abs/2607.12385>

## Prospective Intention Store

Zhao and Wu, “Making Prospective Memory SLM-Shaped: Typed Intention Stores for Small-Model Agents,” arXiv:2609.01272. PIS separates language grounding from a typed intention store and lifecycle operations. Reported scores are reproduction targets, not accepted ground truth.

Primary record: <https://arxiv.org/abs/2609.01272>

As of the initial audit, the paper says code will be released upon acceptance and no official repository was located. Any implementation before an official release must be labeled an independent reimplementation and accompanied by an ambiguity ledger.

## Open comparison questions

- Whether prompting alone improves extraction, monitoring, precision, and update handling consistently.
- Whether PIS gains come from typed persistence, deterministic filtering, extra calls, or unmatched budgets.
- Whether either method transfers beyond one template-generated week.

