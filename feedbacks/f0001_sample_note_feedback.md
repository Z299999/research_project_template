# f0001 — Feedback on the sample note (w00003)

- **Date:** 2026-07-03
- **Source:** [Advisor Name] (meeting / email / margin notes)
- **On:** `writing/w00003_sample_note` — Proposition 1.1 and Figure 1
- **Status:** open

> This is a **sample** feedback record showing the format. In a real project,
> one file per feedback episode; keep the advisor's words verbatim where it
> matters, and turn each point into a checkable action item.

## Points raised

1. **Proposition 1.1(ii).** "Fastest decay rate among ζ ≥ 1" is correct but
   worth stating precisely — give the decay exponent (`ζω` vs. the slower real
   root for ζ > 1) so the "fastest" claim is quantitative, not just asserted.
2. **Figure 1.** Add the critically-damped and overdamped curves (campaigns AB,
   AC) on the same axes; the three-regime contrast is the whole point and one
   panel would carry it better than the underdamped curve alone.
3. **Citation.** One classic reference is fine for a note; if this grows into a
   report, cite the specific control-textbook treatment of second-order response.

## Action items

- [ ] (pt. 1) State the decay exponent explicitly in Prop. 1.1(ii).
- [ ] (pt. 2) Add a `viz.fig_regime_overlay(res_list, out)` to `e00001/src/viz.py`
      and a combined figure; copy it into `w00003/figures/`.
- [ ] (pt. 3) Defer unless the note becomes a report.

## Resolution

_(Fill in when addressed; link the commit that closes each item.)_
