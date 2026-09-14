# v2.1 manuscript replacement paragraphs and Russian defense

Proposed replacement text for author review; the Pages manuscript has not been overwritten. Author: Bagdat Beimzhan. AI-assisted implementation, analysis and semantic review must be disclosed according to submission requirements. No independent annotation or supervisor approval is implied. Detailed evidence: [COMPARISON_RESULTS.md](COMPARISON_RESULTS.md).

## Findings — ready to paste

Earlier prompt-only A0/A1 studies found no observed P1 accuracy benefit: the first pilot gave both methods TP5/FP0/FN0 and Set-F1 1.00; the three-day follow-up gave both TP11/FP0/FN1 and Set-F1 22/23. The follow-up overlapped the pilot and was planned after inspecting it, so these results are not independent pooled replications. Kiodai A2 is a separate PIS-inspired engineering integration, not a relabeling of A1.

The first original-v2 DeepSeek smoke completed its checkpoints but stored no intentions or execution receipts, yielding Set-F1 0. A separately frozen v2.1 repair smoke demonstrated one complete three-task instruction-to-receipt chain with Set-F1 1.00, despite temporary prerequisite and predicate defects. This established narrow development integration feasibility. The following comparison evaluated the frozen v2.1 candidate without further repair or tuning and retained every scoreable failure.

The frozen comparison completed all 36 method-trajectories, 288 checkpoints and 12 matched blocks. Kiodai A2 did not outperform either comparator: mean paired trajectory Set-F1 difference was -0.330556 versus B_ledger and -0.383730 versus A0. This is negative comparative development evidence, with working integration in some traces; it does not establish general inferiority, equivalence, reliability or held-out performance.

| Method | TP | FP | FN | Micro precision | Micro recall | Micro Set-F1 | Mean trajectory Set-F1 |
|---|---|---|---|---|---|---|---|
| A0 | 22 | 6 | 2 | 0.7857 | 0.9167 | 0.8462 | 0.8643 |
| B_ledger | 18 | 4 | 3 | 0.8182 | 0.8571 | 0.8372 | 0.8111 |
| A2 | 12 | 5 | 7 | 0.7059 | 0.6316 | 0.6667 | 0.4806 |

The predeclared family means for A2/B_ledger/A0 were 0.5000/0.7778/1.0000 for hidden conditions, 0.8667/0.8000/0.6000 for visible events, 0/0.6667/0.8571 for cross-day tasks, and 0.5556/1.0000/1.0000 for revisions. The small positive visible-event contrast involved no queries. The one prior smoke-overlap case yielded A2 Set-F1 0, while the other eleven exposed cases retained negative mean contrasts of −0.3000 against B_ledger and −0.3277 against A0. The eleven-case group is not held out.

Each ledger method eventually stored all 27 instructed intentions. A2 completed 12 obligations, B_ledger 18 and A0 22; excluding canceled requests, 12, 6 and 2 remained unfinished. Five A2 and three B_ledger obligations were dependency-blocked at their trigger opportunity. These never-due tasks were not counted as successful completion or silently added to the unchanged official FN metric.

A2 obtained 3 query-supported hidden successes from 18 board checks, compared with B_ledger's 4 from 8 and A0's 6 from 15. The due-opportunity denominators differ because prerequisite failures prevented some later tasks from becoming due. Seven clock queries across the controls merely repeated visible time information. Negative board readings were not automatically labeled unnecessary. More monitoring did not establish improved execution in this comparison.

All 24 ledger trajectories underwent source-linked semantic review, separately from task scoring. Initial prerequisite representation was incomplete in every dependency-bearing case; some unknown records were appropriately quarantined, while others were incorrectly eligible with empty dependencies. Five unsupported menu-derived intention proposals per ledger method were rejected, but incorrect accepted action bindings still occurred. Repaired cue/deadline regressions could coexist with perfect task scores, and one A2 stale-deadline false execution occurred with zero validation failures. These observations show why schema validity, extraction fidelity, monitoring evidence, execution receipts and task scores cannot be treated as interchangeable outcomes.

| Method | Calls | Retries | Input tokens | Output tokens | Recorded call latency (s) | Queries | API-response USD |
|---|---|---|---|---|---|---|---|
| A0 | 117 | 2 | 177,855 | 3,175 | 343.60 | 19 | 0.04047361 |
| B_ledger | 251 | 56 | 910,740 | 44,534 | 2103.46 | 11 | 0.21212084 |
| A2 | 234 | 46 | 843,540 | 42,889 | 1984.12 | 18 | 0.19870816 |

The complete run used 602 calls, 1,932,135 input and 90,598 output tokens. API responses reported $0.45130261, reconciled with the durable ledger under the $20 cumulative ceiling; independent billed cost was unavailable. No model inference followed the study. The system and controls were not compute-matched, and the lower A2 cost than B_ledger accompanies lower accuracy, not a demonstrated efficiency advantage.

## Methods and discussion — ready to paste

The exploratory comparison evaluated one frozen Kiodai v2.1 candidate on all twelve predeclared synthetic development trajectories, grouped into four template families. A0 used the original baseline selector without an explicit intention ledger. B_ledger and A2 shared the extraction prompt, typed store, quarantine, version checks, action selector and receipt lifecycle; B_ledger delegated query decisions to the model, while A2 used the bounded monitoring controller. All methods received the same initial instructions, action interface and eight decision checkpoints per trajectory, with fresh state and their own complete subsequent history. The execution order balanced method position within every family. One repeat yielded twelve matched three-method blocks, not 288 independent observations.

The primary descriptive contrast was fixed before inference as the arithmetic mean of twelve per-trajectory Set-F1 differences, A2 minus B_ledger; A2 minus A0 was secondary. Aggregated TP, FP and FN and their micro precision, recall and Set-F1 are reported separately and do not replace that contrast. Every scoreable mistake and permitted retry was retained. The candidate, scenario bytes, model/provider route, sampling parameters, prompts, validation policy and evaluator remained unchanged throughout execution. The single authorized run was not selectively repeated.

The design is not compute-matched: ledger methods make explicit extraction calls, methods may make additional selections after queries, and their frozen output-token caps differ. More queries therefore require joint interpretation with successful evidence-supported actions, token usage, latency and API-response costs. A query without an immediate task hit is not by itself unnecessary. Saved query evidence supports an observable execution trace; it does not establish the model's internal cognitive cause or causal reliance on that evidence.

Semantic fidelity was audited separately using saved instructions, every accepted and rejected response draft, checkpoint ledgers, action bindings and receipts. The annotations distinguish absent stored intentions following rejected atomic batches, errors in accepted representations, errors in accepted selections and rejected unsupported proposals. Correctly quarantining an unresolved dependency is not itself an error. Repairs are reported even when final task performance is perfect; timing relative to a first due checkpoint remains undefined when a task never became due because its prerequisite failed. These annotations are AI-assisted judgments, not independent human coding or a second evaluator.

All twelve trajectories had been exposed during development, and their variants belong to only four dependent templates. The predeclared overlap split separates the one prior network-smoke scenario from the remaining eleven, which are also exposed. Full history was available. This study cannot establish held-out generalization, broad superiority or equivalence, intrinsic model-memory improvement, autonomous background monitoring or external exactly-once execution. Native completed handles disappear, so independent duplicate side effects remain unidentifiable. Historical pilot, follow-up and smoke results remain separate and are not pooled as independent replications.


The declared primary contrast did not support the monitoring hypothesis. The practical contribution is a reproducible engineering evaluation that records both successful end-to-end operation and failures in prerequisite formation, revision handling, citation correction and action binding. The result does not justify superiority language, broad inferiority claims, a reliable semantic-memory claim or a PIS reproduction claim. The earlier successful smoke remains a feasibility observation, not evidence that the full system was reliable.

## Краткий вывод для статьи

Замороженное сравнение Kiodai v2.1 завершило все 36 запусков методов на 12 открытых синтетических траекториях. Средний Set-F1 по траекториям составил 0,4806 для A2, 0,8111 для B_ledger и 0,8643 для A0. Основная парная разность A2 − B_ledger равна −0,3306; вторичная A2 − A0 — −0,3837. Дополнительные проверки скрытого состояния не дали преимущества на этом наборе. Анализ журналов выявил пропущенные зависимости, возврат к устаревшим условиям и ошибки связывания действий, в том числе при корректном JSON и высоком итоговом балле. Результат подтверждает возможность сквозной интеграции, но не её надёжность и не преимущество A2. Четыре семейства шаблонов, один повтор и заранее известные разработчику сценарии ограничивают обобщение.

## Защита — примерно 60–90 секунд

Мой проект проверяет, может ли агент выполнить поручение позже, когда наступит нужное условие. Я отделяю четыре вопроса: правильно ли сохранено намерение, получены ли нужные наблюдения, выполнено ли действие с подтверждением и каков итоговый балл задачи.

После отдельного ремонта интеграции один проверочный запуск с DeepSeek завершился успешно. Но я не стал считать его доказательством надёжности. Затем был заранее зафиксирован сравнительный протокол: двенадцать траекторий из четырёх семейств, три метода и один повтор. Модель, подсказки, сценарии, повторы запросов и оценивание во время эксперимента не менялись.

Полное сравнение завершилось. У Kiodai A2 средний Set-F1 получился 0,4806, у варианта с тем же списком намерений и выбором запросов моделью — 0,8111, у исходного агента — 0,8643. Основная парная разность отрицательная: минус 0,3306. Поэтому я не утверждаю, что Kiodai улучшил память или превзошёл сравниваемые методы.

Журналы показывают конкретные причины неудачных действий: потерянные зависимости, возврат к старому сроку и неправильное связывание пункта меню с намерением. Иногда после исправления итоговый балл был идеальным, а иногда даже полностью валидные ответы приводили к ошибке. A2 чаще проверял скрытый канал, но выполнил меньше подтверждённых скрытых задач. Все ошибки, повторы и затраты сохранены; стоимость по ответам API составила около 45 центов. Мой результат — работающая в отдельных случаях интеграция и честно измеренные ограничения, а не доказанное преимущество метода.

## Remaining submission tasks

The experiment and reporting are complete after the recorded offline checks. The author still needs to review and integrate these replacement paragraphs and tables into the Pages manuscript, make historical/current claims consistent, check references and required formatting, and export the final submission. Historical results remain intact. No additional experiment or architecture change is proposed.
