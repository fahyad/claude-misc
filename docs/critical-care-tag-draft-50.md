> ⚠️ **SUPERSEDED by [`critical-care-tag-system.md`](critical-care-tag-system.md) (v1.0).**
> These tags were anchored to the old subdeck structure; the v1.0 system re-derives tags
> from the research. Kept for history only.

# Critical Care — 50-card tagging draft (v0.2)

_Proposal only — nothing applied to the collection. A representative sample of 50 real
cards from the `Critical Care` subdecks, each with proposed tags + justification, to
stress-test the schema in `critical-care-tag-schema.md` before bulk tagging._

## Conventions used here (resolved decisions)

- **`cc::` root namespace** (Critical-Care-scoped).
- **No instance tags** (`drug::`/`device::`) — drugs/devices use `cc::type::drug` /
  `cc::type::device` + `cc::sys::…`.
- Core facets on (almost) every card: **`cc::sys::`** (content) + **`cc::task::`** (clinical task).
- Standing conventions applied consistently below:
  - **Normal range / value / parameter recall → `cc::task::physiology`**
    (e.g. PR interval, FiO₂ range, normal CVP).
  - **Indication / contraindication / "when to use" → `cc::task::management`.**
  - **Recognition / interpretation of a finding or waveform → `cc::task::assessment`.**
  - **Definition of a criterion / classification / cut-off → `cc::task::diagnosis`.**

> Two new `sys::`/`task::` values are proposed by this draft (see "Schema adjustments"
> at the end): `cc::sys::cardiovascular::pacing` and `cc::task::pharmacology`.

---

## CVS (24 cards)

**1. "5 Lead ECG color placement"**
`cc::sys::cardiovascular::ecg::lead-placement` · `cc::task::procedure`
— *sys*: lead application is the ECG-setup leaf. *task::procedure*: it's a how-to-set-up skill, not interpretation.

**2. "12 Lead ECG, where to place V1–V6 electrodes?"**
`cc::sys::cardiovascular::ecg::lead-placement` · `cc::task::procedure`
— Same leaf/task as #1; keeps all electrode-placement cards together.

**3. "Is the ECG tracing upward or downward? (current toward positive lead)"**
`cc::sys::cardiovascular::ecg` · `cc::task::physiology`
— *sys*: a general ECG principle, no dysrhythmia leaf. *physiology*: explains the underlying electrophysiology, not a specific reading.

**4. "Which leads are unipolar (augmented)?"**
`cc::sys::cardiovascular::ecg::lead-placement` · `cc::task::physiology`
— Lead theory sits with lead-placement; *physiology* because it's conceptual (how leads are derived).

**5. "Range and what it represents: PR"**
`cc::sys::cardiovascular::ecg::intervals` · `cc::task::physiology`
— *intervals* leaf for PR/QRS/QT. *physiology* per the value-recall convention.

**6. "Causes of T-wave inversion"**
`cc::sys::cardiovascular::ecg::morphology` · `cc::task::diagnosis`
— Finding-based differential → *morphology*; *diagnosis* because it's a differential list for an ECG finding (a mini-sieve card).

**7. "What characterises an atrial flutter on ECG"**
`cc::sys::cardiovascular::ecg::dysrhythmia::atrial` · `cc::task::assessment`
— Rhythm-recognition card → atrial leaf + *assessment* (interpreting the tracing).

**8. "Differentiate atrial fibrillation vs flutter"**
`cc::sys::cardiovascular::ecg::dysrhythmia::atrial` · `cc::task::assessment`
— Comparison of two atrial rhythms; recognition task.

**9. "What does a <100 ms QRS mean?"**
`cc::sys::cardiovascular::ecg::intervals` · `cc::task::physiology`
— Interval interpretation rooted in conduction physiology.

**10. "Physiology of junctional rhythm"**
`cc::sys::cardiovascular::ecg::dysrhythmia::junctional` · `cc::task::pathophysiology`
— Junctional leaf; *pathophysiology* (mechanism of the abnormal rhythm).

**11. "How to classify junctional rhythms (rates)?"**
`cc::sys::cardiovascular::ecg::dysrhythmia::junctional` · `cc::task::diagnosis`
— Same leaf; *diagnosis* because it's a rate-based classification scheme.

**12. "What is a NSVT?"**
`cc::sys::cardiovascular::ecg::dysrhythmia::ventricular` · `cc::task::diagnosis`
— Ventricular leaf; *diagnosis* (definition/criteria of an entity).

**13. "On ECG what characterizes a 1st degree AV block?"**
`cc::sys::cardiovascular::ecg::dysrhythmia::av-block` · `cc::task::assessment`
— AV-block leaf; recognition of the tracing.

**14. "2nd degree AV block type I vs type II (on ECG)"**
`cc::sys::cardiovascular::ecg::dysrhythmia::av-block` · `cc::task::assessment`
— Same leaf; comparative recognition.

**15. "QTc normal range?"**
`cc::sys::cardiovascular::ecg::intervals` · `cc::task::physiology`
— Interval value-recall.

**16. "STEMI vs NSTEMI physiological difference"**
`cc::sys::cardiovascular::acs` · `cc::task::pathophysiology`
— ACS area; mechanism (degree of occlusion).

**17. "Which ECG leads show a LAD infarct?"**  ← polyhierarchy example
`cc::sys::cardiovascular::acs` · `cc::sys::cardiovascular::ecg::morphology` · `cc::task::diagnosis`
— Belongs to *both* ACS and ECG-morphology (localizing infarct by leads); *diagnosis* (territory criteria). Subdecks couldn't do this dual placement.

**18. "Management goals for MI"**
`cc::sys::cardiovascular::acs` · `cc::task::management` · `cc::context::emergency`
— ACS treatment; *management*; time-critical → *context::emergency*.

**19. "Time goal for PCI in MI?"**
`cc::sys::cardiovascular::acs` · `cc::task::management` · `cc::context::emergency`
— A management target (90 min); emergency context.

**20. "Indications for arterial line"**
`cc::sys::cardiovascular::hemodynamics::monitoring` · `cc::type::device` · `cc::task::management`
— Monitoring leaf; *type::device* (art line); *management* per the indication convention.

**21. "Square wave test for arterial line: over damped"**
`cc::sys::cardiovascular::hemodynamics::monitoring` · `cc::type::waveform` · `cc::task::assessment`
— Monitoring; *type::waveform*; recognizing a waveform abnormality → *assessment*.

**22. "Normal central venous pressure"**
`cc::sys::cardiovascular::hemodynamics::monitoring` · `cc::task::physiology`
— Monitoring value-recall.

**23. "Define preload"**
`cc::sys::cardiovascular::hemodynamics::principles` · `cc::task::physiology`
— Principles leaf (concepts, not devices); physiology definition.

**24. "Hypokalemia ECG changes"**  ← flagship polyhierarchy example
`cc::sys::cardiovascular::ecg::morphology` · `cc::sys::electrolytes` · `cc::task::assessment`
— The whole reason for the rebuild: this card is genuinely *both* an ECG-morphology card and an electrolytes card, surfacing in either study session.

---

## Electrolytes / cross-cutting (2 cards)

**25. "Hypocalcemia ECG changes"**
`cc::sys::cardiovascular::ecg::morphology` · `cc::sys::electrolytes` · `cc::task::pathophysiology`
— Dual home like #24; *pathophysiology* because the card explains the Ca²⁺-plateau mechanism behind QT prolongation, not just the finding.

**26. "Hypocalcemia vs hypomagnesemia ECG changes"**
`cc::sys::cardiovascular::ecg::morphology` · `cc::sys::electrolytes` · `cc::task::assessment`
— Comparative recognition across two electrolyte disturbances.

---

## Arrest / ACLS (3 cards)

**27. "Indication for defibrillation"**
`cc::sys::cardiovascular::arrest` · `cc::task::management` · `cc::context::emergency`
— Arrest area; indication → *management*; emergency context.

**28. "Quality compression rate and depth"**
`cc::sys::cardiovascular::arrest` · `cc::task::procedure` · `cc::context::emergency`
— A psychomotor skill → *procedure*.

**29. "Epinephrine MOA" (binds α-1 → vasoconstriction)**
`cc::sys::cardiovascular::arrest` · `cc::type::drug` · `cc::task::pharmacology`
— Used in arrest; *type::drug*; MOA → proposed `cc::task::pharmacology` (see Schema adjustments). Could pair `cc::context::emergency`.

---

## Pacing / Devices (2 cards)

**30. "Pacemaker: what to adjust if failure to capture?"**
`cc::sys::cardiovascular::pacing` · `cc::type::device` · `cc::task::management`
— Pacemaker troubleshooting needs a sys home → proposed `cc::sys::cardiovascular::pacing`; adjusting output is a *management* decision.

**31. "PA catheter: normal SVR"**
`cc::sys::cardiovascular::hemodynamics::monitoring` · `cc::type::device` · `cc::task::physiology`
— PA cath data; value-recall. (Without instance tags, PA-cath cards gather via monitoring + `type::device` + search.)

---

## Respiratory (11 cards)

**32. "What is FiO₂?"**
`cc::sys::respiratory::concepts` · `cc::task::physiology`
— Foundational concept leaf.

**33. "Nasal prongs, FiO₂?"**
`cc::sys::respiratory::oxygen-delivery` · `cc::type::device` · `cc::task::physiology`
— O₂-delivery device parameter → value-recall; *type::device*.

**34. "Non-rebreather mask, FiO₂?"**
`cc::sys::respiratory::oxygen-delivery` · `cc::type::device` · `cc::task::physiology`
— Same pattern as #33.

**35. "Contraindication: nasopharyngeal airway (basal skull #)"**
`cc::sys::respiratory::airway` · `cc::type::device` · `cc::task::management`
— Airway adjunct; contraindication → *management*.

**36. "Endotracheal tube, location of insertion"**
`cc::sys::respiratory::airway` · `cc::type::device` · `cc::task::procedure`
— ETT placement skill.

**37. "What is BiPAP?"**
`cc::sys::respiratory::niv` · `cc::type::device` · `cc::task::physiology`
— NIV concept/definition.

**38. "Contraindication for BiPAP"**
`cc::sys::respiratory::niv` · `cc::task::management`
— When *not* to use → *management*.

**39. "What is PEEP?"**
`cc::sys::respiratory::mech-ventilation` · `cc::task::physiology`
— Vent concept.

**40. "Vent mode: PRVC 16 / PEEP 12 / FiO₂ 60% / Target VT 600"**
`cc::sys::respiratory::mech-ventilation` · `cc::task::assessment`
— Reading/identifying a mode from settings → *assessment* (interpretation).

**41. "GCS objective criteria for intubation"**
`cc::sys::respiratory::intubation` · `cc::task::diagnosis`
— Intubation; *diagnosis* (a decision criterion/cut-off, GCS<8).

**42. "pH criteria for intubation"**  ← polyhierarchy example
`cc::sys::respiratory::intubation` · `cc::sys::acid-base` · `cc::task::diagnosis`
— Both an intubation-criteria card and an acid-base card.

**43. "What are the 3 steps + timing in fast-track extubation?"**
`cc::sys::respiratory::weaning` · `cc::task::management`
— Weaning protocol → *management*.

---

## Acid-base / GI (3 cards)

**44. "What is base excess?"**
`cc::sys::acid-base` · `cc::task::physiology`
— Acid-base concept/definition (now its own sys area, un-bundled from GI).

**45. "Difference between anion-gap vs non-anion-gap acidosis"**
`cc::sys::acid-base` · `cc::task::pathophysiology`
— Mechanism-based comparison of acidosis types.

**46. "What are the two types of small bowel obstruction?"**
`cc::sys::gi` · `cc::task::pathophysiology`
— True GI content; mechanical vs functional → *pathophysiology*.

---

## Endocrine (1 card)

**47. "Intervention for DKA"**  ← was mis-shelved in GI/ABG with a foreign tag
`cc::sys::endocrine::diabetes` · `cc::task::management` · `cc::type::drug`
— Relocated to endocrine; management protocol; involves insulin/fluids → *type::drug*. (Old foreign tag `Patho_Pharm::Diabetes` dropped.)

---

## Renal (1 card)

**48. "Stage 1 AKI creatinine and urine output"**
`cc::sys::renal` · `cc::task::diagnosis`
— Renal; a staging criterion → *diagnosis*.

---

## Perioperative / Heme (2 cards)

**49. "Expected side effects of CPB"**
`cc::sys::perioperative` · `cc::task::complication` · `cc::context::post-op`
— Cardiopulmonary-bypass sequelae → *complication*; post-op context.

**50. "Coagulation: PLT / INR / aPTT normal values"**
`cc::sys::hematology::coagulation` · `cc::task::physiology`
— Lab value-recall; heme/coag area.

---

## Coverage check

| Source subdeck | Cards sampled |
| --- | --- |
| CVS | 24 (#1–24) + electrolytes #25–26 + arrest #27–29 + pacing #30 + PA cath #31 |
| Respiratory | 11 (#32–43) |
| GI/ABG → acid-base + gi | 3 (#44–46) |
| Pharmacology (folded into CVS/endocrine) | drug cards #29, #47 |
| GU → renal | 1 (#48) |
| Surgery/Post-op | 2 (#49–50) |

Most cards landed on **2–3 tags** — fast enough to actually maintain (directly addressing
the "people under-tag" risk from the research).

---

## Schema adjustments surfaced by this draft

Tagging real cards exposed gaps in v0.1 — proposed refinements:

1. **Add `cc::task::pharmacology`.** Drug *mechanism-of-action* cards (#29 epinephrine,
   amiodarone, adenosine) don't fit `physiology` vs `management` cleanly. A dedicated
   pharmacology task is cleaner and gathers all MOA cards. *(Alternative: fold MOA into
   `physiology` — your call.)*
2. **Add `cc::sys::cardiovascular::pacing`.** Pacemaker troubleshooting (#30, and the
   capture/sense/pace cards) had no home once the Devices subdeck dissolves.
3. **Add `cc::type::waveform`** (used #21) — distinguishes waveform-interpretation cards
   (ART/CVP/thermodilution) from plain values; useful given how image/waveform-heavy this
   deck is.
4. **Confirm the value-recall rule.** "Normal range/value" → `cc::task::physiology` was
   applied to many cards (#5, #9, #15, #22, #31, #33–34, #50). If you'd rather these be
   their own facet (e.g. `cc::task::reference-value`), easy to switch — but it adds a facet.
5. **Homeless edge case to decide:** generic nursing skills like "Order to draw labs (tube
   order)" don't fit any `sys::` cleanly. Options: a `cc::sys::nursing-skills` catch-all, or
   leave under `cc::sys::perioperative`. Flagged, not resolved.

## Suggested next step

If these tags look right, I can **expand to the full 258-note mapping** as a reviewable
table + an apply-script (AnkiConnect `addTags`, run locally), built on the finalized facet
list above.
