# Browser verification

2026-09-08, local URL http://127.0.0.1:8765, default MOCK server.

Observed through the browser UI:

- Page renders as a local research dashboard with A0/A1 columns and a visible MOCK label.
- Start created a distinct paired run and enabled Advance timeline.
- Time scenario: empty actions at 16:00, 16:30 and 16:59; both condition-neutral scripts selected the project-submission handle at 17:00.
- Reveal displayed evaluator TP=1, FP=0, FN=0 after the response was fixed.
- Fifth step completed the trajectory; Reset returned to the initial screen.
- Hidden-condition scenario: allowed teacher_feed query exposed ABSTRACT ACCEPTED at 12:30, followed by the abstract action; after completion no task action was selected.
- The RECORDED selector showed no genuine saved LIVE runs. It did not relabel a displayed MOCK trajectory.
- The actual-request/response and full-conversation disclosures are available for inspection.
- Dashboard typography and the side-by-side cards were visually inspected in a screenshot.

The HTTP exercise separately verified all six scenarios, early-reveal rejection, reset, disabled-live rejection, and a 25-file MOCK archive. See http-demo.json and demo-export.zip. No paid model calls were made. Successful replay and transport edge cases use temporary test fixtures, not genuine research results.
