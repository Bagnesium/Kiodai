"""Reproduce new comparison documents from saved, reviewed evidence; no inference."""
import json
from pathlib import Path
ROOT=Path.cwd().resolve(); RUN=ROOT/'results/v2_1/comparison-v1'; V=ROOT/'artifacts/verification/v21-comparison-live-20260911'
r=json.loads((RUN/'comparison_report_reviewed.json').read_text()); a=json.loads((RUN/'supplementary_analysis.json').read_text()); m=a['methods']; methods=['A0','B_ledger','A2']
assert a['status']=='completed' and a['matched_blocks']==12
assert all(c['diagnostics']['semantic_review']['status']=='reviewed' for c in r['cases'] if c['method']!='A0')
primary=a['paired']['A2 minus B_ledger']['declared_mean_difference'];secondary=a['paired']['A2 minus A0']['declared_mean_difference']
def num(x,d=4):return 'undefined' if x is None else f'{x:.{d}f}'
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+['| '+' | '.join(str(v) for v in row)+' |' for row in rows])
def metric_table():return table(['Method','TP','FP','FN','Micro precision','Micro recall','Micro Set-F1','Mean trajectory Set-F1'],[[k,*[m[k]['micro'][x] for x in ['tp','fp','fn']],*[num(m[k]['micro'][x]) for x in ['precision','recall','set_f1']],num(m[k]['mean_trajectory_set_f1'])] for k in methods])
trajectory_rows=[]
for t in dict.fromkeys(c['trajectory'] for c in r['cases']):
 cs={c['method']:c for c in r['cases'] if c['trajectory']==t};trajectory_rows.append([t,*[num(cs[k]['set_f1']) for k in methods],num(cs['A2']['set_f1']-cs['B_ledger']['set_f1']),num(cs['A2']['set_f1']-cs['A0']['set_f1'])])
family_rows=[]
for family in r['families']:
 family_rows.append([family,*[num(sum(c['set_f1'] for c in r['cases'] if c['family']==family and c['method']==k)/3) for k in methods],*[num(r['families'][family]['comparisons'][key]['declared_mean_difference']) for key in ['A2 minus B_ledger','A2 minus A0']]])
overlap_rows=[]
for flag in (True,False):
 cs=[c for c in r['cases'] if c['prior_network_smoke']==flag]; n=len(cs)//3
 overlap_rows.append(['Prior smoke overlap' if flag else 'Other exposed cases',n,*[num(sum(c['set_f1'] for c in cs if c['method']==k)/n) for k in methods],*[num(r['smoke_overlap'][str(flag)]['comparisons'][key]['declared_mean_difference']) for key in ['A2 minus B_ledger','A2 minus A0']]])
resources=table(['Method','Calls','Retries','Input tokens','Output tokens','Recorded call latency (s)','Queries','API-response USD'],[[k,m[k]['model_calls'],m[k]['retries'],f"{m[k]['input_tokens']:,}",f"{m[k]['output_tokens']:,}",num(m[k]['latency_seconds'],2),m[k]['tool_queries'],num(m[k]['api_response_cost_usd'],8)] for k in methods])
obligations=table(['Method','Instructed','Ever due','Dependency-blocked at trigger','Completed','Unfinished incl. canceled','Unfinished excl. canceled','Canceled'],[[k,*[m[k][x] for x in ['total_instructed_obligations','unique_obligations_ever_due','unique_obligations_blocked_at_trigger','completed_obligations','unfinished_including_canceled','unfinished_not_canceled','canceled_obligations']]] for k in methods])
failures=table(['Method','Extract schema / application failures','Selection schema / application failures','Extract / selection retries','Accepted operation responses / empty updates','Fail-closed checkpoints','Executions / successful / failed receipts'],[[k,'N/A' if k=='A0' else f"{m[k]['validation_failure_stages'].get('extract/structure',0)} / {m[k]['validation_failure_stages'].get('extract/application',0)}",f"{m[k]['validation_failure_stages'].get(('baseline' if k=='A0' else 'select')+'/structure',0)} / {m[k]['validation_failure_stages'].get(('baseline' if k=='A0' else 'select')+'/application',0)}",('N/A / '+str(m[k]['retries'])) if k=='A0' else f"{m[k]['retry_kinds'].get('extract',0)} / {m[k]['retry_kinds'].get('select',0)}",'N/A' if k=='A0' else f"{m[k]['extraction_accepted_operation_responses']} / {m[k]['extraction_accepted_empty_updates']}",m[k]['fail_closed_checkpoints'],f"{m[k]['task_executions']} / {m[k]['successful_simulator_receipts']} / {m[k]['failed_simulator_receipts']}"] for k in methods])
semantic=table(['Post-hoc annotation category','B_ledger','A2'],[[key,m['B_ledger']['semantic_review_findings'].get(key,0),m['A2']['semantic_review_findings'].get(key,0)] for key in ['missing_intention','missing_prerequisite','missing_required_field','incorrect_trigger','incorrect_binding','unsupported_intention','other']])
headline=f'The frozen comparison completed all 36 method-trajectories, 288 checkpoints and 12 matched blocks. Kiodai A2 did not outperform either comparator: mean paired trajectory Set-F1 difference was {primary:.6f} versus B_ledger and {secondary:.6f} versus A0. This is negative comparative development evidence, with working integration in some traces; it does not establish general inferiority, equivalence, reliability or held-out performance.'
report=f'''# Genuine v2.1-comparison-v1 results — 11 September 2026

{headline}

## Execution, authorization and preservation

The exact authorized command ran once from a clean checkout at `cd0ce89e10d036918d1af06e5f5f2140930a0981`:

```bash
python3 scripts/run_v21_comparison.py --live --authorize-study v2.1-comparison-v1 --budget-usd 20.00 --env-file .env
```

Started {a['started_at_utc']}; finished {a['finished_at_utc']}. Candidate `959db38dac8b68f63ecf79420dcd53bea2278cf2`, support `832d6ff1e3f43f9086da9d6aac33b79f5212ecdc`, and manifest SHA-256 `bfaf52df48553e35978f39f406fd5eb3d78c918a5ac2713a0a169746f23036d5` remain unchanged. The exact free preflight passed. Read-only funding checks at 07:57:12 UTC found $21.85988004 remaining key allowance and $21.92988004 account credit, both above the frozen $19.95251712 requirement. No account setting was changed. The earlier funding-blocked attempt made zero model calls; this was the first actual execution.

The 59 frozen source/config/scenario files, 442 preparation records and 65 provenance records match. Every recorded request matches the pinned configuration, and every response reports the pinned DeepSeek V3.1 model and Novita provider. No fallback occurred. Provider enforcement of every schema or sampling parameter remains unverified. Maximum serialized request size was {a['verification']['maximum_request_bytes']:,} bytes versus the frozen 48,000-byte gate. Saved requests contain no canonical private scenario/evaluator identifiers or due-set fields. All official scores, case hashes, complete eight-checkpoint traces, frozen method order and accounting entries reproduce. No source, prompt, scenario, retry or scorer was changed; no failure was excluded, no run restarted, no selective repeat or extra inference occurred.

All **445 original runner files** were archived and hash-verified before adding post-hoc annotations. Original reports and raw traces remain intact. The frozen specification retains its historical preparation-time authorization/status fields; actual authorization and execution are documented separately. Historical smokes, preparation outputs, A0/A1 studies and the prior funding-block record remain historical evidence, not independent repeats pooled into this study.

## Primary results

{metric_table()}

The headline uses the **arithmetic mean of twelve paired trajectory Set-F1 differences**, not a difference of micro scores: **A2 − B_ledger = {primary:.6f}**, secondary **A2 − A0 = {secondary:.6f}**. Coverage is 12/12 for both. A2 wins 2, ties 4 and loses 6 pairs against B_ledger; it wins 2, ties 3 and loses 7 against A0. These are descriptive counts, not independent significance tests. The micro metrics sum unchanged official TP/FP/FN first; their different denominators and weighting do not replace the frozen estimand.

{table(['Trajectory','A0 F1','B_ledger F1','A2 F1','A2 − B_ledger','A2 − A0'],trajectory_rows)}

Per-trajectory TP/FP/FN, precision, recall, costs, failures and receipts are in `results/v2_1/comparison-v1/comparison_report_reviewed.json` and the original generated comparison table.

## Predeclared family and exposure breakdowns

Each family has three exposed variants. Entries below are mean trajectory F1, not micro F1.

{table(['Family','A0','B_ledger','A2','A2 − B_ledger','A2 − A0'],family_rows)}

A2's small visible-event advantage occurred with zero tool queries in that family; it is not evidence that polling caused the improvement. Cross-day performance was zero in all three A2 cases, while B_ledger completed two and A0 completed the instructed tasks in all three (with false actions in one). Revision failures include abstention after a citation retry and an accepted stale-deadline execution.

{table(['Exposure group','Trajectories','A0','B_ledger','A2','A2 − B_ledger','A2 − A0'],overlap_rows)}

The sole smoke-overlap case is `v2_hidden_91320`. The remaining eleven are still exposed development cases. Negative mean differences persist in that predeclared group; this is not a post-hoc exclusion or a held-out test.

## Obligations and execution

{obligations}

Never-due dependent obligations are not successful completions and do not automatically add official FN. In this run the five blocked A2 obligations comprise two hidden sealing tasks and all three cross-day sealing tasks. Canceled obligations explain three legitimate non-completions per method. Official FN counts remain 2/3/7 for A0/B_ledger/A2; active unfinished counts are 2/6/12. Official commission counters are not generic counts of every early action; the complete FP/receipt and updated-task diagnostics are retained.

{failures}

All 602 requests have responses; transport errors and unknown-cost attempts are zero. Total invalid responses are 2/64/52 and retries 2/56/46 for A0/B_ledger/A2. Counts include both initial and second-attempt failures. Accepted empty updates are decisions to make no ledger change; they do not establish correct extraction. The ledger methods each eventually store 27 instructed intentions. A0 has no extraction layer, so its empty store is not a zero-error extraction result.

## Monitoring evidence and its costs

A0 made 15 hidden-board queries and 4 clock queries; B_ledger made 8 board and 3 clock queries; A2 made 18 board queries and no clock queries. Same-checkpoint query-supported hidden hits were **6, 4 and 3**, respectively. A2 additionally had one due hidden miss and one false hidden action. No scored hidden hit lacked identifiable query support. Hidden due opportunities were 6/4/4 and differ because prerequisite failures suppress later due tasks; comparing hit ratios alone would conceal those failures.

A2 made ten more board queries than B_ledger (+125%) and three more than A0 (+20%), yet recorded fewer supported hidden successes. Across all families A2 made seven more queries than B_ledger and one fewer than A0. Manual review identified **4 A0 and 3 B_ledger clock queries** that repeated the already visible current time and stopwatch; no A2 query was demonstrably informationally redundant. All hidden-board checks addressed unfinished obligations. This does not establish optimal polling or prove that negative checks were necessary; the number without an immediate hit is only a proxy. Evidence support is observable, not proof of internal causal reliance.

The methods are not compute-matched. A2 used 17 fewer model calls and $0.01341268 less API-reported cost than B_ledger, despite more queries; B_ledger's query decisions and retries required additional selections. A2 used twice A0's model calls and $0.15823455 more reported cost, with substantially lower mean F1. There is no observed efficiency/superiority claim from these totals.

## Semantic fidelity, independently of task score

All **24/24 ledger cases** and all **12 A0 behavioral traces** were reviewed using saved instructions, every response draft, checkpoint snapshots, bindings and receipts. No case remains unreviewed. Review is AI-assisted and has no independent human annotator; internal understanding and causal explanations remain uncertain. Source-linked annotations and repair timing are in `semantic_review.json` and `comparison_report_reviewed.json`.

{semantic}

These are annotation findings, **not independent error trials or an error-rate comparison**. Layers distinguish 10/6 absent stored intentions after rejected batches, 15/12 accepted representation findings, 1/2 accepted binding findings, and 5/5 rejected unsupported-intention proposals for B_ledger/A2. A2 also has one explicitly labeled intermediate regression repaired within an atomic transaction before any selector sees it. Composite predicate loss counts once; repeated unsupported proposals count by checkpoint. Invalid draft fields and retries have separate raw-attempt counts above.

- In all six dependency-bearing cases per ledger method, initial structured prerequisite information was incomplete. Some records incorrectly became eligible with empty dependencies; others were safely quarantined as unknown but omitted the required unresolved-prerequisite text from `condition`, even though their source quotations retained it. Initial quarantine itself is not an error. Repairs and delays are explicitly recorded.
- Both methods proposed five unsupported spare-sample obligations from action menus. All ten proposals were rejected; **zero unsupported/distractor intentions were stored**. This does not mean distractor execution was impossible: both ledger methods bound a spare-sample handle to the genuine registration intention in cross-day 91331 and attached its failed receipt to that real record.
- Accepted cue regressions affected two A2 and all three B_ledger visible-event cases, restoring a superseded lantern cue after a triangle update. Premature sealing received failed receipts; subsequent correction sometimes yielded a final high score.
- All three revision variants in both ledger methods had accepted deadline regressions. A2 91300 had a second regression that caused a premature registration before successful repair; all sixteen model responses in that case passed validation. A2 91302 also regressed and immediately repaired within a single later transaction; that intermediate value was not a selector input.
- B_ledger 91322 canceled registration based only on the clock, without a cancellation instruction. A2 91321 accepted a sealing handle bound to the registration intention after rejecting the ineligible sealing ID. Correct citation spans and valid versions did not establish correct action identity.
- Quarantine appeared in 5 B_ledger cases (9 checkpoint snapshots) and 2 A2 cases (2 snapshots); no final record remained quarantined. That is not proof that all obligations were completed or all earlier representations faithful. Repairs for never-due tasks have undefined pre-due timing. In A2 cross-day 91330/91332 and revision 91302, a correct-time selection was rejected for a stale citation and the retry abstained despite correct stored fields.

These observations separate **extraction/storage working in some cases**, **monitoring obtaining relevant observations**, **execution producing genuine simulator receipts**, and **task score**. The integration runs, but its accepted semantics and execution are unreliable on this development set. Receipt-based lifecycle mechanics do not guarantee a correct binding or trigger. Superseded-version rejection is a mechanical invariant; it cannot detect an obsolete instruction stored as a new version. Independent duplicate side effects remain unidentifiable because native completed handles disappear.

{(V/'behavioral_trace.md').read_text()}

## Resources and billing status

{resources}

Totals: **602 calls**, **1,932,135 input tokens**, **90,598 output tokens**, **48 tool queries**, and **$0.45130261 API-response-reported cost**. Recorded call latency sums to {sum(m[k]['latency_seconds'] for k in methods):.2f} seconds; wall-clock execution lasted 73 minutes 55.688 seconds. Latency is the sum of recorded calls including failed validation attempts, not a compute-matched efficiency estimate. The durable guard reserved **$9.13802496** under the **$20.00 cumulative ceiling**; reservations are not charges. All response-reported costs reconcile with the ledger; **independently verified billed cost remains unavailable**. Account credit checks before the run are funding evidence, not independent study billing. No remaining credit or unused authorization was spent afterward.

## Relationship to earlier evidence

The failed original v2 DeepSeek smoke had an empty ledger, no queries or receipts and TP0/FP0/FN2 (24 calls, API $0.01525668). The separately frozen v2.1 repair smoke populated three intentions, queried seven times and completed three tasks with Set-F1 1.00 (17 calls, API $0.016737), while still showing prerequisite/predicate defects. Those original files and conclusions remain intact.

On the identical smoke-overlap scenario in this comparison, A2 again scored 0 but with a different trace: three intentions eventually stored, six board queries, and no executed task or receipt because early extraction failures missed registration and later selections failed validation. Thus the repair made integration feasible; the one successful smoke did not establish reproducible task success or robust extraction. This study is not a controlled repair-versus-original causal comparison, and prior smokes are not pooled with its twelve blocks.

## Interpretation and submission scope

The frozen monitoring hypothesis received **no observed improvement** on its declared primary contrast. A2 had lower mean trajectory Set-F1 than both controls, with a small visible-event advantage and negative hidden, cross-day and revision contrasts. Four dependent template families, exposed scenarios, one repeat, full-history access and unequal compute prevent broad generalization, significance, equivalence or intrinsic-memory claims. Checkpoints and model calls are not replications. The contribution is a recorded engineering evaluation with localized failure evidence, not demonstrated A2 superiority or a faithful PIS reproduction.

Manuscript replacement paragraphs and Russian defense: `docs/v2_1/FINDINGS_AND_DEFENSE.md`. The Pages manuscript was not overwritten. Remaining submission work is author review and integration of those paragraphs/tables, consistency of historical/current wording, reference/format checks and final submission export; no additional experiment is proposed or authorized.

## Artifacts, replay and offline reproduction

- Original recording: `results/v2_1/comparison-v1/`; original `comparison_report.json/.md` remain unchanged.
- Reviewed report: `comparison_report_reviewed.json/.md`; source-linked `semantic_review.json`, `baseline_behavior_review.json`; `supplementary_analysis.json` contains reconciled metrics, every validation failure and accounting.
- Original 445-file ZIP: `artifacts/v2_1/comparison_v1_original_run.zip`; SHA-256 inventory: `research/v2_1/live_comparison_v1_inventory.json`. Restore only absent files; refuse to overwrite any differing local bytes.
- Authorization, funding, preflight, offline verification and reproducible analysis helper: `artifacts/verification/v21-comparison-live-20260911/`.
- Prior funding-block documents are retained unchanged in `prior_funding_block_original.zip` and commit `cd0ce89`; its old inventory is commit/archive-bound because current handoff/CLAIMS/V2 status documents necessarily change.

Run from `/Users/bagnesium/Documents/GitHub/Kiodai`:

```bash
python3 scripts/report_v21_comparison.py --study results/v2_1/comparison-v1 --annotations results/v2_1/comparison-v1/semantic_review.json
python3 artifacts/verification/v21-comparison-live-20260911/audit_saved_comparison.py results/v2_1/comparison-v1/semantic_review.json
python3 scripts/run_v21_comparison.py --preflight
python3 scripts/verify_benchmark_integrity.py
python3 -m unittest discover -s tests -v
python3 scripts/serve_v2.py --study results/v2_1/comparison-v1 --port 8772
```

Open `http://127.0.0.1:8772/`. Select any trajectory, method and checkpoint; the existing viewer labels genuine LIVE artifacts **RECORDED**, with inference disabled. Evaluator reveal remains separate. The viewer cannot launch a paid run. Offline verification passed: 162 tests, 164 protected hashes, Python compilation, the free frozen preflight, and 72 recorded-viewer checkpoint checks. Detailed outcomes are recorded under the verification directory; no new smoke was run.
'''
(ROOT/'docs/v2_1/COMPARISON_RESULTS.md').write_text(report)
ru=f'Замороженное сравнение Kiodai v2.1 завершило все 36 запусков методов на 12 открытых синтетических траекториях. Средний Set-F1 по траекториям составил 0,4806 для A2, 0,8111 для B_ledger и 0,8643 для A0. Основная парная разность A2 − B_ledger равна −0,3306; вторичная A2 − A0 — −0,3837. Дополнительные проверки скрытого состояния не дали преимущества на этом наборе. Анализ журналов выявил пропущенные зависимости, возврат к устаревшим условиям и ошибки связывания действий, в том числе при корректном JSON и высоком итоговом балле. Результат подтверждает возможность сквозной интеграции, но не её надёжность и не преимущество A2. Четыре семейства шаблонов, один повтор и заранее известные разработчику сценарии ограничивают обобщение.'
findings=f'''# v2.1 manuscript replacement paragraphs and Russian defense

Proposed replacement text for author review; the Pages manuscript has not been overwritten. Author: Bagdat Beimzhan. AI-assisted implementation, analysis and semantic review must be disclosed according to submission requirements. No independent annotation or supervisor approval is implied. Detailed evidence: [COMPARISON_RESULTS.md](COMPARISON_RESULTS.md).

## Findings — ready to paste

Earlier prompt-only A0/A1 studies found no observed P1 accuracy benefit: the first pilot gave both methods TP5/FP0/FN0 and Set-F1 1.00; the three-day follow-up gave both TP11/FP0/FN1 and Set-F1 22/23. The follow-up overlapped the pilot and was planned after inspecting it, so these results are not independent pooled replications. Kiodai A2 is a separate PIS-inspired engineering integration, not a relabeling of A1.

The first original-v2 DeepSeek smoke completed its checkpoints but stored no intentions or execution receipts, yielding Set-F1 0. A separately frozen v2.1 repair smoke demonstrated one complete three-task instruction-to-receipt chain with Set-F1 1.00, despite temporary prerequisite and predicate defects. This established narrow development integration feasibility. The following comparison evaluated the frozen v2.1 candidate without further repair or tuning and retained every scoreable failure.

{headline}

{metric_table()}

The predeclared family means for A2/B_ledger/A0 were 0.5000/0.7778/1.0000 for hidden conditions, 0.8667/0.8000/0.6000 for visible events, 0/0.6667/0.8571 for cross-day tasks, and 0.5556/1.0000/1.0000 for revisions. The small positive visible-event contrast involved no queries. The one prior smoke-overlap case yielded A2 Set-F1 0, while the other eleven exposed cases retained negative mean contrasts of −0.3000 against B_ledger and −0.3277 against A0. The eleven-case group is not held out.

Each ledger method eventually stored all 27 instructed intentions. A2 completed 12 obligations, B_ledger 18 and A0 22; excluding canceled requests, 12, 6 and 2 remained unfinished. Five A2 and three B_ledger obligations were dependency-blocked at their trigger opportunity. These never-due tasks were not counted as successful completion or silently added to the unchanged official FN metric.

A2 obtained 3 query-supported hidden successes from 18 board checks, compared with B_ledger's 4 from 8 and A0's 6 from 15. The due-opportunity denominators differ because prerequisite failures prevented some later tasks from becoming due. Seven clock queries across the controls merely repeated visible time information. Negative board readings were not automatically labeled unnecessary. More monitoring did not establish improved execution in this comparison.

All 24 ledger trajectories underwent source-linked semantic review, separately from task scoring. Initial prerequisite representation was incomplete in every dependency-bearing case; some unknown records were appropriately quarantined, while others were incorrectly eligible with empty dependencies. Five unsupported menu-derived intention proposals per ledger method were rejected, but incorrect accepted action bindings still occurred. Repaired cue/deadline regressions could coexist with perfect task scores, and one A2 stale-deadline false execution occurred with zero validation failures. These observations show why schema validity, extraction fidelity, monitoring evidence, execution receipts and task scores cannot be treated as interchangeable outcomes.

{resources}

The complete run used 602 calls, 1,932,135 input and 90,598 output tokens. API responses reported $0.45130261, reconciled with the durable ledger under the $20 cumulative ceiling; independent billed cost was unavailable. No model inference followed the study. The system and controls were not compute-matched, and the lower A2 cost than B_ledger accompanies lower accuracy, not a demonstrated efficiency advantage.

## Methods and discussion — ready to paste

{(V/'methods_background.md').read_text().split('\n\n',1)[1]}

The declared primary contrast did not support the monitoring hypothesis. The practical contribution is a reproducible engineering evaluation that records both successful end-to-end operation and failures in prerequisite formation, revision handling, citation correction and action binding. The result does not justify superiority language, broad inferiority claims, a reliable semantic-memory claim or a PIS reproduction claim. The earlier successful smoke remains a feasibility observation, not evidence that the full system was reliable.

## Краткий вывод для статьи

{ru}

## Защита — примерно 60–90 секунд

Мой проект проверяет, может ли агент выполнить поручение позже, когда наступит нужное условие. Я отделяю четыре вопроса: правильно ли сохранено намерение, получены ли нужные наблюдения, выполнено ли действие с подтверждением и каков итоговый балл задачи.

После отдельного ремонта интеграции один проверочный запуск с DeepSeek завершился успешно. Но я не стал считать его доказательством надёжности. Затем был заранее зафиксирован сравнительный протокол: двенадцать траекторий из четырёх семейств, три метода и один повтор. Модель, подсказки, сценарии, повторы запросов и оценивание во время эксперимента не менялись.

Полное сравнение завершилось. У Kiodai A2 средний Set-F1 получился 0,4806, у варианта с тем же списком намерений и выбором запросов моделью — 0,8111, у исходного агента — 0,8643. Основная парная разность отрицательная: минус 0,3306. Поэтому я не утверждаю, что Kiodai улучшил память или превзошёл сравниваемые методы.

Журналы показывают конкретные причины неудачных действий: потерянные зависимости, возврат к старому сроку и неправильное связывание пункта меню с намерением. Иногда после исправления итоговый балл был идеальным, а иногда даже полностью валидные ответы приводили к ошибке. A2 чаще проверял скрытый канал, но выполнил меньше подтверждённых скрытых задач. Все ошибки, повторы и затраты сохранены; стоимость по ответам API составила около 45 центов. Мой результат — работающая в отдельных случаях интеграция и честно измеренные ограничения, а не доказанное преимущество метода.

## Remaining submission tasks

The experiment and reporting are complete after the recorded offline checks. The author still needs to review and integrate these replacement paragraphs and tables into the Pages manuscript, make historical/current claims consistent, check references and required formatting, and export the final submission. Historical results remain intact. No additional experiment or architecture change is proposed.
'''
(ROOT/'docs/v2_1/FINDINGS_AND_DEFENSE.md').write_text(findings)
print('Wrote docs/v2_1/COMPARISON_RESULTS.md and FINDINGS_AND_DEFENSE.md')
