# Research Status

- Updated: 2026-09-04
- Completed: Harness guardrails; one frozen P1 instruction; equivalent Codex/Claude skill; one independently authored and frozen three-day development suite; paired DeepSeek V3.1 A0/A1 configurations; cost preflight; 25 local tests; protected-file and development-suite integrity verification; skill validation.
- Current blocker: Paid/network execution requires explicit user approval and an `OPENROUTER_API_KEY`.
- Active hypothesis: P1 will materially improve paired development Set-F1 and task recall without a material increase in false-positive actions.
- Latest verified result: No A0/A1 model result exists. The development scenario validates and is solvable under perfect play; it contains 20 steps, 14 intentions, and 12 due actions. All 164 protected files match the frozen hashes, all 25 local tests pass, and the six-step deterministic mock smoke run completed with zero network cost. A maximum-query/maximum-retry offline stress preflight projected $0.1886 for the pair, below the $0.30 approval ceiling.
- Next action: Stop for review. Run the paired A0/A1 development experiment only after explicit approval and availability of `OPENROUTER_API_KEY`.
- Outstanding uncertainty: Prompt-only internal state may not persist reliably because the strict action schema does not expose a textual ledger across turns. Heartbeat remains unsupported in the clean runner and is intentionally excluded from both conditions.
