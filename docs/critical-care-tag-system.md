# Critical Care — tagging system v1.2 (two-axis, flat)

_Proposal only — nothing applied to the collection. Supersedes v0.x, v1.0, and v1.1.
v1.2 renames the two axes to **`system`** and **`knowledge`** and flattens every value to a
single level (no system has sub-levels), so all tags are exactly `cc::<axis>::<value>`._

## v1.3 refinements (from the post-application review — see critical-care-tag-review.md)
- **physiology vs pathophysiology rule enforced:** a disease/disorder *entity* (its
  definition, types/classification, or mechanism) → `pathophysiology`; *normal* function,
  normal values, concepts/formulas, and drug MOA → `physiology`. Definitions of non-disease
  concepts/devices (PEEP, BiPAP, cardiac index) stay `physiology`.
- **Dual knowledge allowed:** a card that genuinely bundles two knowledge types may carry
  two `cc::knowledge::` tags (e.g. nitroglycerin = `physiology` + `management`). Kept rare.
- **Cross-system pass:** systems applied from *back* content too (CPB → acid-base +
  fluid-electrolyte + hematologic; PPV→CO → +cardiovascular; DKA → +fluid-electrolyte +
  acid-base; ABG-based intubation criteria → +acid-base). 12 cards now span >1 system.

## What changed v1.1 → v1.2
- Axis 1 renamed `topic` → **`system`**.
- Axis 2 renamed `know` → **`knowledge`** (fully spelled out).
- Removed the 4th-level sub-values from `cardiovascular` and `respiratory` — **every system
  is now flat.** Result: no tag exceeds 3 levels (`cc::system::cardiovascular`,
  `cc::knowledge::management`).

## Overlap review (unchanged rationale — why exactly these two axes)

| Facet pair | Overlap | Decision |
| --- | --- | --- |
| `knowledge::` × old `sem::` | **High** — `management`↔procedure/drug/device, `diagnostics`↔finding/measurement | dropped `sem::` |
| `system::` × `knowledge::` | **None** — domain vs. knowledge-type are independent | **the two axes** |
| `cause::`, `acuity::`, `flag::` | not content-defining | optional sprinkles |

---

## The two axes (every card = one of each)

> **Q1 — What body system / domain is it about?** → `cc::system::…`
> **Q2 — What kind of knowledge is it?** → `cc::knowledge::…`

### Axis 1 · `cc::system::` — clinical domain (flat controlled vocabulary)

One level, no sub-values. Names borrow MeSH-style controlled vocabulary (research §2.3,
§4.3); flat/broad per §4.4.

```
cc::system::cardiovascular
cc::system::respiratory
cc::system::renal
cc::system::gastrointestinal
cc::system::endocrine
cc::system::neurological
cc::system::hematologic
cc::system::acid-base
cc::system::fluid-electrolyte
cc::system::integumentary
cc::system::perioperative
cc::system::multisystem
```
A card may carry **two systems** when it genuinely spans domains (deliberate polyhierarchy,
§2.1) — e.g. an electrolyte-induced ECG change is `cardiovascular` + `fluid-electrolyte`.

### Axis 2 · `cc::knowledge::` — knowledge type (illness-script / disease-schema)

The cognitive axis (research §1.1–1.2). One value per card. Flat.

```
cc::knowledge::physiology        normal function, definitions, normal values, drug MOA
cc::knowledge::etiology          causes, risk factors, precipitants
cc::knowledge::pathophysiology   how the disease/derangement works
cc::knowledge::manifestation     what the patient/body SHOWS (symptoms, physical signs)
cc::knowledge::diagnostics       tests, labs, values, criteria, classification, ECG/waveform interpretation
cc::knowledge::management        treatment, drugs (indication/dose), procedures, algorithms
cc::knowledge::complications     sequelae, adverse effects, prognosis
```

**Disambiguation rules** (so the single pick has no overlap):
- **physiology vs pathophysiology** — *normal* function/values/drug-MOA → `physiology`; how a
  disease *derails* it → `pathophysiology`.
- **etiology vs pathophysiology** — *what causes/precipitates* → `etiology`; *the mechanism*
  of the derangement → `pathophysiology`.
- **manifestation vs diagnostics** — something the body/patient *shows* (symptom/physical
  sign) → `manifestation`; a *test/lab/ECG/waveform/criterion* you obtain or interpret →
  `diagnostics`. _(So "ECG of AV block" = diagnostics; "signs of low cardiac output" = manifestation.)_
- **management vs diagnostics** — an *action that treats/operates* (drug dose, procedure,
  device use) → `management`; a *test/criterion that informs* → `diagnostics`.
- **complications vs manifestation** — *downstream* sequelae / adverse effect / prognosis →
  `complications`; *presenting* features of the condition → `manifestation`.

**Drug cards:** MOA → `physiology`; indication/dose/prep → `management`; side-effects →
`complications`.

---

## Depth rule (≤3 levels, counting `cc::`)

Every tag is exactly **3 levels**: `cc::system::cardiovascular`, `cc::knowledge::management`.
Nothing deeper. ✓

---

## Optional sprinkles (NOT part of the 2-decision core)

Add only when obviously useful; never required:
- `cc::acuity::acute | chronic | emergency` (§1.3)
- `cc::flag::high-yield | weak | leech | image-fix` (workflow)
- `cc::cause::vascular | infective | …` — only on differential/cause cards (§3.1; aids
  breadth not accuracy, §3.2)
- Per-entity tags (`drug::amiodarone`, `device::pa-catheter`) remain **deferred**.

---

## Re-tagged sample under v1.2 (two tags each)

**Contrast — v1.1 → v1.2 (relabel + flatten):**

| Card | v1.1 | v1.2 |
| --- | --- | --- |
| "Atrial flutter recognition" | `topic::cardiovascular::rhythm` · `know::diagnostics` | `cc::system::cardiovascular` · `cc::knowledge::diagnostics` |
| "Define preload" | `topic::cardiovascular::hemodynamics` · `know::physiology` | `cc::system::cardiovascular` · `cc::knowledge::physiology` |
| "What is PEEP?" | `topic::respiratory::ventilation` · `know::physiology` | `cc::system::respiratory` · `cc::knowledge::physiology` |

**Fresh sample across the deck:**

1. **5-lead ECG colour placement** — `cc::system::cardiovascular` · `cc::knowledge::management`
2. **PR interval range & meaning** — `cc::system::cardiovascular` · `cc::knowledge::physiology`
3. **1st-degree AV block recognition** — `cc::system::cardiovascular` · `cc::knowledge::diagnostics`
4. **STEMI vs NSTEMI mechanism** — `cc::system::cardiovascular` · `cc::knowledge::pathophysiology`
5. **Which leads show an LAD infarct?** — `cc::system::cardiovascular` · `cc::knowledge::diagnostics`
6. **Management goals for MI** — `cc::system::cardiovascular` · `cc::knowledge::management`
7. **Define preload** — `cc::system::cardiovascular` · `cc::knowledge::physiology`
8. **Normal CVP** — `cc::system::cardiovascular` · `cc::knowledge::physiology`
9. **Hypokalemia ECG changes** — `cc::system::cardiovascular` · `cc::system::fluid-electrolyte` · `cc::knowledge::manifestation` _(two systems)_
10. **Treatment for pericarditis** — `cc::system::cardiovascular` · `cc::knowledge::management`
11. **Acute heart failure — what is it?** — `cc::system::cardiovascular` · `cc::knowledge::pathophysiology`
12. **Causes of hypertensive crisis** — `cc::system::cardiovascular` · `cc::knowledge::etiology`
13. **Pacemaker: fix failure to capture** — `cc::system::cardiovascular` · `cc::knowledge::management`
14. **What is FiO₂?** — `cc::system::respiratory` · `cc::knowledge::physiology`
15. **Contraindication: nasopharyngeal airway** — `cc::system::respiratory` · `cc::knowledge::management`
16. **What is PEEP?** — `cc::system::respiratory` · `cc::knowledge::physiology`
17. **pH criteria for intubation** — `cc::system::respiratory` · `cc::system::acid-base` · `cc::knowledge::diagnostics` _(two systems)_
18. **Fast-track extubation steps** — `cc::system::respiratory` · `cc::knowledge::management`
19. **Anion-gap vs non-anion-gap acidosis** — `cc::system::acid-base` · `cc::knowledge::pathophysiology`
20. **Intervention for DKA** — `cc::system::endocrine` · `cc::knowledge::management`
21. **Stage 1 AKI criteria** — `cc::system::renal` · `cc::knowledge::diagnostics`
22. **Expected side effects of CPB** — `cc::system::perioperative` · `cc::knowledge::complications`
23. **Coagulation normal values (PLT/INR/aPTT)** — `cc::system::hematologic` · `cc::knowledge::physiology`
24. **Blanchable vs non-blanchable erythema** — `cc::system::integumentary` · `cc::knowledge::diagnostics`

Almost every card = **2 tags**; a few = 3 (genuinely cross-system).

---

## How you study a sub-topic (two-axis search)

- All cardiology diagnostics (ECG, hemodynamics, etc.): `tag:cc::system::cardiovascular tag:cc::knowledge::diagnostics`
- All drug mechanisms: `tag:cc::knowledge::physiology` + text search for the drug
- Everything to *treat* in cardiology: `tag:cc::system::cardiovascular tag:cc::knowledge::management`
- Electrolyte cards anywhere: `tag:cc::system::fluid-electrolyte`

_Trade-off of flattening:_ you can no longer isolate *just* arrhythmia vs *just* coronary
within cardiovascular by tag alone — that drill-down now uses text search, or the deferred
per-entity tag layer if it proves necessary.

## Honest limits (from the research)

- The disease-schema **order** isn't a validated learning sequence (§1.2) — `knowledge::` is
  an *organizing* axis, not a study order.
- Flattening trades fine drill-down for **maintainability** (§4.5) — the intended trade.

## Next step

If the two axes look right, I'll **map all 258 notes** to v1.2 tags as a reviewable table +
an AnkiConnect apply-script to run locally, then a tag-consistency audit.
