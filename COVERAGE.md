# Coverage established by the first LIVE pilot

The original result remains **one matched pair, 16 calls, A0=A1: TP=5, FP=0, FN=0, Set-F1=1.00; difference 0**. A1 used 5,360 additional input tokens. Saved API-response costs total $0.00765034; independently verified billing is unavailable. This table is based on actual requests, selections and evaluator records, not scenario names or passing tests.

| Capability | Status | Actual evidence and scope |
|---|---|---|
| Time-triggered execution | **Tested live** | Monday `dev_m_s3` / 09:40: both select humidity logging; evaluator TP=1. `dev_m_s6` / 11:20: both select the two corrected tasks; TP=2. |
| Event-triggered execution | **Tested live** | `dev_m_s2`: both seal the case on the loading bell. `dev_m_s3`: neither releases the envelope on the blue-circle lure; both release it on the blue hexagon at `dev_m_s5`. |
| Cancellation | **Tested live** | Cancellation is visible at `dev_m_s2`; the canceled proof remains in the offered menu at its exact disposal cue in `dev_m_s5`. Neither condition selects it; no false action is recorded. |
| Rescheduling and repeated updates | **Tested live** | Visible moves 10:10→10:50→11:00→11:20 at `dev_m_s2`/`dev_m_s4`. Both refrain at `dev_m_s4`, `dev_m_s5`, `dev_m_s5b` and act at `dev_m_s6`. |
| Retention across distracting interactions | **Tested live — limited within-day case** | The initial header gives the 09:40 intention; `dev_m_s1` contains unrelated delivery-slip activity and `dev_m_s2` concerns other intentions before correct selection at `dev_m_s3`. Full conversation and action-text menus remain visible. This is not strong long-delay or cross-day evidence. |
| Hidden-channel monitoring | **Demonstrated only in mock mode** | Both LIVE manifests and all 16 calls contain zero queries; Monday has no required hidden positive event. Saved MOCK `mock-pair-891566d658aa` queries `teacher_feed` at `demo_step_2` (under review) and `demo_step_4` (accepted), then selects the abstract action only on acceptance. |
| Negative steps with no action due | **Tested live** | Both return an empty task set at `dev_m_s1`, `dev_m_s4`, `dev_m_s5b`, `dev_m_s7`; each evaluator record has empty due/selected sets and TP=FP=FN=0. These steps are not independent experiments. |
| Long-delay / cross-day retention | **Not tested** | Monday mentions a Wednesday instruction, but the LIVE pilot ends Monday. There is no live retrieval or execution at the later trigger. |

Live evidence folders (JSONL line order follows the eight scheduled steps):

- [A0](results/kiodai/live-pair-42433e00474b/live-A0-20260908T164420-7848b46b/): `steps.jsonl` gives visible history/tools/actions; `raw_model_calls.jsonl` records the eight responses; `evaluator.jsonl` gives separate due/false/missed sets.
- [A1](results/kiodai/live-pair-42433e00474b/live-A1-20260908T164420-2fdeb6e6/): the same evidence types; all task selections and evaluator outcomes match A0.
- [Mock hidden-channel demonstration](results/kiodai/mock-pair-891566d658aa/pair.json): genuine saved software-fixture traces, explicitly **MOCK**, not model evidence.

Completion/duplicate prevention is not independently established: PM-Bench removes completed handles, and frozen P1 assumes completion after selection rather than robustly confirming successful execution. Heartbeat is disabled; neither live nor mock traces establish autonomous background monitoring.

The first pair, both earlier TLS startup failures and original report snapshots are retained in [pilot1-preserved-20260908.zip](artifacts/verification/pilot1-preserved-20260908.zip), with a SHA-256 inventory in [pilot1_preservation_v1.json](research/pilot1_preservation_v1.json). The follow-up uses a separate output root and report and must not replace or be pooled with this result.
