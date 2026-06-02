# Critical Care — tagging system v1.1 (two-axis)

_Proposal only — nothing applied to the collection. Supersedes the v0.x drafts and the
v1.0 three-axis version. **v1.1 collapses to TWO orthogonal axes** after an overlap review,
to lower the per-card tagging effort (research §4.5: people under-tag when the barrier is
high)._

## What changed from v1.0 → v1.1

v1.0 had three core facets: `topic` + `know` + `sem`. Review showed **`know::` and `sem::`
substantially overlap** (a "management" card is almost always a procedure/drug/device; a
"diagnostics" card is almost always a finding/measurement; disease cards are disorders). A
third axis that's predictable from the second adds upkeep without adding retrieval power —
so `sem::` is **dropped**. `cause::`/`acuity::`/`flag::` are demoted to optional. Result:
**every card needs exactly two decisions.**

## Overlap review (why two axes, and which two)

| Facet pair | Overlap | Decision |
| --- | --- | --- |
| `know::` × `sem::` | **High** — `management`↔`procedure/drug/device`, `diagnostics`↔`finding/measurement`, disease-types↔`disorder` | **Drop `sem::`** |
| `topic::` × `know::` | **None** — domain vs. knowledge-type are independent | **Keep both (the two axes)** |
| `cause::` × `know::etiology` | `cause::` ⊂ `etiology` | Optional refinement only |
| `acuity::`, `flag::` × all | Orthogonal but not content-defining | Optional, sprinkle when obvious |

---

## The two axes (every card = one of each)

Two independent questions, no overlap, so the decision is fast:

> **Q1 — What is it about?** → `cc::topic::…`
> **Q2 — What kind of knowledge is it?** → `cc::know::…`

### Axis 1 · `cc::topic::` — clinical domain (broad-shallow, controlled vocabulary)

Body-system / domain. **≤2 content levels** below the axis (level-2 only for the big
domains, grouped by function). Names borrow MeSH-style controlled vocabulary (research
§2.3, §4.3); broad-shallow per §4.4.

```
cc::topic::cardiovascular     ::rhythm  ::coronary  ::hemodynamics  ::structural  ::failure
cc::topic::respiratory        ::oxygenation  ::airway  ::ventilation
cc::topic::renal
cc::topic::gastrointestinal
cc::topic::endocrine
cc::topic::neurological
cc::topic::hematologic
cc::topic::acid-base
cc::topic::fluid-electrolyte
cc::topic::integumentary
cc::topic::perioperative
cc::topic::multisystem
```
A card may carry **two topics** when it genuinely spans domains (deliberate polyhierarchy,
§2.1) — e.g. an electrolyte-induced ECG change is `cardiovascular::rhythm` + `fluid-electrolyte`.

### Axis 2 · `cc::know::` — knowledge type (illness-script / disease-schema)

The cognitive axis (research §1.1–1.2). One value per card. Flat (1 level).

```
cc::know::physiology        normal function, definitions, normal values, drug MOA
cc::know::etiology          causes, risk factors, precipitants
cc::know::pathophysiology   how the disease/derangement works
cc::know::manifestation     what the patient/body SHOWS (symptoms, physical signs)
cc::know::diagnostics       tests, labs, values, criteria, classification, ECG/waveform interpretation
cc::know::management        treatment, drugs (indication/dose), procedures, algorithms
cc::know::complications     sequelae, adverse effects, prognosis
```

**Disambiguation rules** (so the single pick is unambiguous — the point of "no overlap"):
- **physiology vs pathophysiology** — *normal* function/values/drug-MOA → `physiology`; how a
  disease *derails* it → `pathophysiology`.
- **etiology vs pathophysiology** — *what causes/precipitates* → `etiology`; *the mechanism*
  of the derangement → `pathophysiology`.
- **manifestation vs diagnostics** — something the body/patient *shows* (a symptom or physical
  sign) → `manifestation`; a *test/lab/ECG/waveform/criterion* you obtain or interpret →
  `diagnostics`. _(So "ECG of AV block" = diagnostics; "signs of low cardiac output" = manifestation.)_
- **management vs diagnostics** — an *action that treats/operates* (drug dose, procedure,
  device use) → `management`; a *test/criterion that informs* → `diagnostics`.
- **complications vs manifestation** — *downstream* sequelae / adverse effect / prognosis →
  `complications`; *presenting* features of the condition → `manifestation`.

**Drug cards** (research-derived, unchanged): MOA → `physiology`; indication/dose/prep →
`management`; side-effects → `complications`.

---

## Depth rule (you endorsed: ≤3 levels)

`cc::` is the **scope root** (your namespace decision) — like a drive letter, not a
semantic level. Below it, meaningful depth is capped at **3**:
- deepest topic = `cc::topic::cardiovascular::rhythm` → `topic / cardiovascular / rhythm` = 3 ✓
- `cc::know::management` → `know / management` = 2 ✓

_(If you'd rather count `cc::` itself as a level, say so and I'll flatten — e.g. drop the
`topic::`/`know::` axis word so it's `cc::cardiovascular::rhythm`.)_

---

## Optional sprinkles (NOT part of the 2-decision core)

Add only when obviously useful; never required, so they don't raise the barrier:
- `cc::acuity::acute | chronic | emergency` — semantic qualifier (§1.3)
- `cc::flag::high-yield | weak | leech | image-fix` — personal workflow (housekeeping)
- `cc::cause::vascular | infective | …` — only on differential/cause cards, refines
  `know::etiology` (surgical sieve, §3.1; note: aids breadth, not accuracy, §3.2)
- Per-entity tags (`drug::amiodarone`, `device::pa-catheter`) remain **deferred** (your
  decision) — recover specific-entity gathering via search until/if needed.

---

## Re-tagged sample under v1.1 (two tags each)

**Simplification contrast — v1.0 (3 axes) → v1.1 (2 axes):**

| Card | v1.0 | v1.1 |
| --- | --- | --- |
| "Amiodarone MOA" | `topic::cv::rhythm` · `know::physiology` · `sem::drug` | `cc::topic::cardiovascular::rhythm` · `cc::know::physiology` |
| "Square-wave: over-damped" | `topic::cv::hemodynamics` · `know::diagnostics` · `sem::finding` | `cc::topic::cardiovascular::hemodynamics` · `cc::know::diagnostics` |
| "Indication for defibrillation" | `topic::cv::rhythm` · `know::management` · `sem::procedure` · `acuity::emergency` | `cc::topic::cardiovascular::rhythm` · `cc::know::management` _(+`acuity::emergency` if wanted)_ |

**Fresh sample across the deck:**

1. **5-lead ECG colour placement** — `cc::topic::cardiovascular::rhythm` · `cc::know::management`
2. **PR interval range & meaning** — `cc::topic::cardiovascular::rhythm` · `cc::know::physiology`
3. **1st-degree AV block recognition** — `cc::topic::cardiovascular::rhythm` · `cc::know::diagnostics`
4. **STEMI vs NSTEMI mechanism** — `cc::topic::cardiovascular::coronary` · `cc::know::pathophysiology`
5. **Which leads show an LAD infarct?** — `cc::topic::cardiovascular::coronary` · `cc::topic::cardiovascular::rhythm` · `cc::know::diagnostics` _(two topics)_
6. **Management goals for MI** — `cc::topic::cardiovascular::coronary` · `cc::know::management`
7. **Define preload** — `cc::topic::cardiovascular::hemodynamics` · `cc::know::physiology`
8. **Normal CVP** — `cc::topic::cardiovascular::hemodynamics` · `cc::know::physiology`
9. **Hypokalemia ECG changes** — `cc::topic::cardiovascular::rhythm` · `cc::topic::fluid-electrolyte` · `cc::know::manifestation`
10. **Treatment for pericarditis** — `cc::topic::cardiovascular::structural` · `cc::know::management`
11. **Acute heart failure — what is it?** — `cc::topic::cardiovascular::failure` · `cc::know::pathophysiology`
12. **Causes of hypertensive crisis** — `cc::topic::cardiovascular` · `cc::know::etiology`
13. **Pacemaker: fix failure to capture** — `cc::topic::cardiovascular::rhythm` · `cc::know::management`
14. **What is FiO₂?** — `cc::topic::respiratory::oxygenation` · `cc::know::physiology`
15. **Contraindication: nasopharyngeal airway** — `cc::topic::respiratory::airway` · `cc::know::management`
16. **What is PEEP?** — `cc::topic::respiratory::ventilation` · `cc::know::physiology`
17. **pH criteria for intubation** — `cc::topic::respiratory::ventilation` · `cc::topic::acid-base` · `cc::know::diagnostics`
18. **Fast-track extubation steps** — `cc::topic::respiratory::ventilation` · `cc::know::management`
19. **Anion-gap vs non-anion-gap acidosis** — `cc::topic::acid-base` · `cc::know::pathophysiology`
20. **Intervention for DKA** — `cc::topic::endocrine` · `cc::know::management`
21. **Stage 1 AKI criteria** — `cc::topic::renal` · `cc::know::diagnostics`
22. **Expected side effects of CPB** — `cc::topic::perioperative` · `cc::know::complications`
23. **Coagulation normal values (PLT/INR/aPTT)** — `cc::topic::hematologic` · `cc::know::physiology`
24. **Blanchable vs non-blanchable erythema** — `cc::topic::integumentary` · `cc::know::diagnostics`

Almost every card = **2 tags**; a handful = 3 (dual-topic). That's the low-friction target.

---

## How you still study a sub-topic (two-axis search)

- Arrhythmia recognition: `tag:cc::topic::cardiovascular::rhythm tag:cc::know::diagnostics`
- All drug mechanisms: `tag:cc::know::physiology` + text search for the drug
- Everything to *treat* in cardiology: `tag:cc::topic::cardiovascular::* tag:cc::know::management`
- Electrolyte cards anywhere: `tag:cc::topic::fluid-electrolyte`

## Honest limits (from the research)

- The disease-schema **order** isn't a validated learning sequence (§1.2) — `know::` is an
  *organizing* axis, not a study order.
- Two axes trade some precision (no built-in entity gathering) for **maintainability** —
  the right trade given §4.5. Recover entity drill-down later via the deferred tag layer.

## Next step

If the two axes look right, I'll **map all 258 notes** to v1.1 tags as a reviewable table +
an AnkiConnect apply-script to run locally, then a tag-consistency audit.
