# v2.1 comparison — stopped before inference

On 11 September 2026, the user authorized exactly `v2.1-comparison-v1` once with a cumulative $20.00 paid-inference ceiling, conditional on the frozen preflight and external funding checks. The study was **not started** because both the key allowance and account credit were insufficient for the declared conservative allowance. This is a funding-gate record, not a model experiment result.

The exact offline command `python3 scripts/run_v21_comparison.py --preflight` passed at commit `d7e92d38fc333846670ae196c9ee37f9d616f61a`. All 59 frozen source/configuration/scenario hashes, 442 preparation files and 65 provenance files matched. Candidate behavior remains `959db38dac8b68f63ecf79420dcd53bea2278cf2`. The comparison manifest SHA-256 remains `bfaf52df48553e35978f39f406fd5eb3d78c918a5ac2713a0a169746f23036d5`; no implementation, prompt, scenario, scoring, provider, retry or frozen manifest change was made.

At **2026-09-11 07:06:07 UTC**, authenticated read-only `GET /api/v1/key` and `GET /api/v1/credits` both returned HTTP 200 with verified TLS. Only whitelisted metadata was saved; no credentials or authorization headers were printed or persisted.

| Funding check | USD |
|---|---:|
| Authorized local ceiling | 20.00000000 |
| Required conservative allowance | 19.95251712 |
| Current key limit | 5.00000000 |
| Remaining key allowance | 4.92988004 |
| Account total credits | 10.00000000 |
| Account total usage | 0.07011996 |
| Available account credit: total credits minus total usage | 9.92988004 |
| Key allowance shortfall | 15.02263708 |
| Account credit shortfall | 10.02263708 |

The local $20 flag does not increase either external restriction. The lower expected-cost projection does not satisfy the user's requirement to fund the entire conservative allowance. No account/key settings, purchases, top-ups or budget controls were changed. The route check inside the LIVE runner was not reached; current route availability was not established by this funding check.

| Condition | Completed method-trajectories | TP / FP / FN | Precision / recall / Set-F1 |
|---|---:|---|---|
| A0 | 0/12 | unavailable | unavailable |
| B_ledger | 0/12 | unavailable | unavailable |
| A2 | 0/12 | unavailable | unavailable |

There are **0/12 usable matched blocks**, no completed checkpoints, and no primary A2−B_ledger or secondary A2−A0 paired estimate. No comparative model outputs exist to inspect for extraction, monitoring, query necessity, execution or concealed semantic errors. No difference between methods was observed because none ran. Missing task scores are unavailable, not zero-performance scores. Family and smoke-overlap breakdowns likewise have no observations.

This check made **zero model calls**, used **zero inference tokens**, and incurred **$0 in paid inference**. No model-response cost or model latency exists. The account endpoints report aggregate funding and prior usage; these figures are not independently verified study billing. No study accounting database or reservations were created, and the exact LIVE command was never invoked. There is no interrupted attempt to resume or reset. No background retry or additional inference was scheduled.

## Manuscript status and limits

The frozen comparison was withheld before model inference because the available API-key allowance and account credit could not cover its conservative funding requirement. Consequently, it supplies no comparative evidence about A0, B_ledger or A2. The earlier successful v2.1 smoke still establishes only narrow development integration feasibility; it does not establish A2 superiority, reliable semantic extraction, equivalence, or held-out generalization. The planned design remains 12 exposed variants from four dependent template families, one repeat, with methods that are not compute matched; its 288 checkpoints and 36 method-trajectories must not be treated as independent replications.

Замороженное сравнение v2.1 не было запущено: остаток лимита API-ключа ($4,93) и баланс аккаунта ($9,93) не покрывали консервативный бюджет $19,95. Поэтому сравнительные метрики A0, B_ledger и A2 отсутствуют. Предыдущий smoke-тест подтверждает лишь техническую возможность работы интеграции в одном сценарии разработки и не доказывает преимущество A2 или надёжность семантического извлечения намерений.

## Evidence and replay status

Sanitized metadata, the read-only check script, exact authorization, offline preflight, gate record and verification logs are preserved under [`artifacts/verification/v21-comparison-funding-block-20260911/`](../../artifacts/verification/v21-comparison-funding-block-20260911/). The frozen preparation artifacts and both earlier smoke recordings remain unchanged.

Offline verification after the documentation update passed: **162 tests**, **164 protected-file hashes**, Python compilation, frozen comparison preflight and `git diff --check`. The evidence inventory records SHA-256 hashes; these checks used no network model inference.

`results/v2_1/comparison-v1/` remains absent. A genuine comparison cannot be offered in RECORDED mode without an actual run. No MOCK data was relabeled or substituted. The previous successful smoke can still be replayed through the existing interface, without inference:

```bash
python3 scripts/serve_v2.py --port 8771 --study results/v2_1/deepseek-smoke-v1
```

Then open http://127.0.0.1:8771/. This is the **prior A2 smoke**, not the unexecuted comparison. No dashboard redesign or new comparison recording was made.
