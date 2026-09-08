# Frozen Development Suite v1

The development suite is independently authored and contains no released-week task IDs, labels, action text, or copied scenarios. It has three virtual days, 20 steps, 14 intentions, two cancellations, three reschedule operations on one intention, two overrides, one dependency, one hidden state channel, 12 due actions under perfect play, and no embedded `groundtruth` fields.

Authoritative scenario: `data/development/prospective_memory_dev_v1.json`

| Required case | Frozen location | Intended stress |
|---|---|---|
| Simple time trigger | Monday `dev_m_s3` | Execute humidity log exactly at 09:40 |
| Simple event trigger | Monday `dev_m_s2` | Execute only on the loading bell |
| Long-delay intention | Monday `dev_m_s1` to Wednesday `dev_w_s4` | Retain an intention for two intervening days |
| Cancellation | Monday `dev_m_s2` and `dev_m_s5` | Suppress proof recycling after its later cue |
| Rescheduling | Monday `dev_m_s2` | Replace 10:10 with 10:50 |
| Multiple reschedules | Monday `dev_m_s4` through `dev_m_s5b` | Resolve 10:50 to 11:00 to 11:20 and suppress obsolete times |
| Override | Tuesday `dev_t_s2`, `dev_t_s3`, and `dev_t_s6` | Ignore amber and wait for violet approval |
| Conflicting instructions | Monday `dev_m_s4` | Apply the explicitly later correction and corrected status wording |
| Irrelevant distraction | Monday `dev_m_s7`, Tuesday `dev_t_s4` | Retain intentions without inventing actions |
| Similar false trigger | Monday `dev_m_s3`, Wednesday `dev_w_s2` | Reject circle and scrape near-matches |
| Simultaneous intentions | Monday `dev_m_s6`, Tuesday `dev_t_s5` | Select the complete due set |
| Hidden-state monitoring | Tuesday sensor-board events | Query the relevant channel and distinguish nearly stable from stable |
| Task that must not execute | Canceled proof and placard tasks | Suppress even when their exact cues later occur |
| Duplicate-execution trap | Monday `dev_m_s7`, Wednesday `dev_w_s5` | Do not re-fire completed or obsolete intentions after textual reminders |
| Cross-day intention | Tuesday `dev_t_s7` to Wednesday `dev_w_s3` | Retain a next-day event intention |

The live action schema removes completed handles from subsequent step menus, so the duplicate trap measures semantic re-firing through similar offered actions and stale versions; it cannot test resubmitting an unavailable completed handle. That benchmark constraint must be reported rather than hidden.

