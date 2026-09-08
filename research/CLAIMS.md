# Claims Register

| Claim | Supporting experiment | Supporting metric | Confidence | Limitation | Safe wording |
|---|---|---|---|---|---|
| The original released artifacts can be rescored locally | Released-log replay audit | Deterministic aggregate reconstruction | Preliminary | Does not validate live model execution | “Released trajectories are locally scoreable.” |
| The original live runner is leakage-free | None | None | Rejected | Oracle due-set fallback exists | “The released runner contains a potential oracle fallback.” |
| One static skill improves prospective memory | Frozen first-day pilot, `live-pair-42433e00474b`, one matched pair | A0=A1: TP=5, FP=0, FN=0, Set-F1=1.00; paired difference 0 | No improvement observed in this pilot | One development scenario; baseline ceiling; no general equivalence or superiority established | “The exploratory pilot found no accuracy benefit from P1; both conditions reached the score ceiling.” |
| PIS is reproduced | Not run | None | None | Official code not located | No reproduction claim permitted. |
