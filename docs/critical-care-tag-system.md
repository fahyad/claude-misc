# Critical Care — tagging system v1.0 (research-derived, from scratch)

_Proposal only — nothing applied to the collection. This **supersedes** the v0.x drafts
(`critical-care-tag-schema.md`, `critical-care-tag-draft-50.md`), which were anchored to
the old subdeck hierarchy. This version is built **from the research findings up**, not
from the existing structure._

## Why this is a clean redesign, not a relabel

The v0.x `sys::` tree (`cardiovascular::ecg::dysrhythmia::atrial`) was the **old 5-level
subdeck path with new punctuation** — it inherited the legacy *topical silo* as its
skeleton. The research says the powerful axes are **orthogonal facets**, not one deep
topic tree. So v1.0 keeps the topic axis deliberately **broad and shallow** and moves the
organizing weight onto two research-grounded facets the old system lacked: a **disease-
schema / illness-script** axis and a **semantic-type** axis. Depth that used to live in the
tree is now expressed by *combining* shallow facets (the LOINC/PMEST principle).

## Facet → research provenance

Every facet traces to a finding in `medical-knowledge-organization-research.md`:

| Facet | Derives from (research §) | Confidence of basis |
| --- | --- | --- |
| `cc::know::` (knowledge type) | Illness scripts / disease schema (§1.1–1.2) | high (scripts) / thin (exact order) |
| `cc::sem::` (semantic type) | UMLS small semantic-type layer (§2.4) | moderate–high |
| `cc::topic::` (domain, shallow) | Faceted/multi-axial + broad-shallow (§2.2, §4.4) + controlled vocab (§2.3, §4.3) | high |
| `cc::cause::` (etiology category) | Surgical sieve / VINDICATE (§3.1–3.2) | high (as *organizing aid*; breadth≠accuracy) |
| `cc::acuity::` (qualifier) | Semantic qualifiers (§1.3) | high for recall |
| `cc::flag::` (workflow) | Behavioral reality / maintenance (§4.5, §2.6) | n/a (housekeeping) |

> **`cc::` root** = scope namespace (your resolved decision). **No per-entity instance
> tags** (your resolved decision) — entities are captured by `sem::` type + topic + search.

---

## The two CORE facets (on almost every card)

### `cc::know::` — knowledge type (the illness-script / disease-schema axis)

*What kind of knowledge is this card?* This is the central new idea: it slots each card
into an illness-script component. The disease-schema **order** is not a proven learning
sequence (§1.2 — evidence thin), so we use it purely as an **organizing axis**, not a study
order.

```
cc::know::physiology        normal function, concepts, normal values, drug MOA/pharmacodynamics
cc::know::etiology          causes, risk factors, enabling conditions
cc::know::pathophysiology   disease mechanism (how it goes wrong)
cc::know::manifestation     signs, symptoms, clinical features ("consequences")
cc::know::diagnostics       investigations, labs, criteria, classification, monitoring & waveform/ECG interpretation
cc::know::management        treatment, interventions, algorithms, indications, drug dose/prep, procedures/skills
cc::know::complications     sequelae, expected adverse effects, prognosis
```

**Note on drug cards (answers the earlier MOA question, research-derived):** the
knowledge-encapsulation model (§1.1) treats pharmacology as part of the *physiologic*
knowledge underlying scripts. So:
- drug **mechanism of action** → `cc::know::physiology`
- drug **indication / dose / prep** → `cc::know::management`
- drug **side effects** → `cc::know::complications`
No separate "pharmacology" facet is needed — the `know::` axis absorbs it cleanly.

### `cc::sem::` — semantic type (the UMLS-style type layer, §2.4)

*What kind of THING is the card's subject?* A small, fixed, controlled set (UMLS overlays
~135 types on millions of concepts; we use ~7). Each card gets **one** `sem::`.

```
cc::sem::disorder      a disease/condition/syndrome
cc::sem::finding       a sign, symptom, or observable (incl. ECG/waveform findings)
cc::sem::procedure     an intervention/technique/skill
cc::sem::drug          a pharmacologic substance
cc::sem::device        equipment/hardware
cc::sem::measurement   a lab, value, parameter, or formula
cc::sem::concept       a physiologic principle (no single disorder/device subject)
```

---

## The SUPPORTING facet

### `cc::topic::` — clinical domain (broad-shallow, controlled vocabulary)

Deliberately **≤2 levels** (§4.4 broad-shallow). Level-1 names borrow MeSH-style
body-system controlled vocabulary (§2.3, §4.3). Level-2 exists only for the few large
domains, and is grouped by **function**, not by the old subdeck path.

```
cc::topic::cardiovascular            ::rhythm  ::coronary  ::hemodynamics  ::structural  ::failure
cc::topic::respiratory               ::oxygenation  ::airway  ::ventilation
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

A card may carry **two topics** (deliberate polyhierarchy, §2.1) — e.g. an electrolyte-
induced ECG change is both `cardiovascular::rhythm` and `fluid-electrolyte`.

---

## OPTIONAL facets (use only when they add a real retrieval path)

### `cc::cause::` — etiology category (surgical sieve / VINDICATE, §3.1)
Apply **only to cards whose content is about causes/differentials**. Research caveat:
sieves increase *breadth* of differentials but not diagnostic *accuracy* (§3.2) — so this
is an organizing aid, used sparingly, not a reasoning crutch.
```
cc::cause::vascular  ::infective  ::inflammatory  ::neoplastic  ::degenerative
cc::cause::iatrogenic  ::congenital  ::autoimmune  ::traumatic  ::metabolic
cc::cause::endocrine  ::idiopathic  ::functional
```

### `cc::acuity::` — semantic qualifier (§1.3)
The one qualifier axis that earns its keep in critical care.
```
cc::acuity::acute   cc::acuity::chronic   cc::acuity::emergency
```

### `cc::flag::` — personal workflow (housekeeping, not content)
```
cc::flag::high-yield   cc::flag::weak   cc::flag::leech   cc::flag::image-fix
```

---

## Naming rules (controlled vocabulary, §2.3 / §4.3 / §2.5)

- `::` hierarchy · **all lowercase** · **hyphens** for spaces · **singular** nouns.
- Fixed value lists above are the controlled vocabulary — don't coin variants ad hoc.
- **Canonical form:** when combining facets, always order them `topic → know → sem →
  (cause/acuity/flag)` in your own notes (§2.5 — one canonical form avoids the
  post-coordination error trap).
- Typical card = **3 tags** (`topic` + `know` + `sem`); complex card = 4–5. Keeping it
  ~3 is deliberate, to survive the "people under-tag" finding (§4.5).

---

## Re-tagged sample under v1.0 (with a few old→new contrasts)

**Contrast set — same cards, old v0.2 vs new v1.0:**

| Card | v0.2 (legacy-anchored) | v1.0 (research-derived) |
| --- | --- | --- |
| "Atrial flutter on ECG" | `sys::cardiovascular::ecg::dysrhythmia::atrial` + `task::assessment` | `cc::topic::cardiovascular::rhythm` · `cc::know::diagnostics` · `cc::sem::finding` |
| "Amiodarone MOA" | `sys::…::dysrhythmia` + `type::drug` + `task::pathophysiology` | `cc::topic::cardiovascular::rhythm` · `cc::know::physiology` · `cc::sem::drug` |
| "Normal CVP" | `sys::…::hemodynamics::monitoring` + `task::physiology` | `cc::topic::cardiovascular::hemodynamics` · `cc::know::physiology` · `cc::sem::measurement` |
| "Causes of T-wave inversion" | `sys::…::ecg::morphology` + `task::diagnosis` | `cc::topic::cardiovascular::rhythm` · `cc::know::etiology` · `cc::sem::finding` |

**Fresh sample across the deck (v1.0):**

1. **"5-lead ECG colour placement"** — `cc::topic::cardiovascular::rhythm` · `cc::know::management` · `cc::sem::procedure`
   *Setting up monitoring is a skill → management + procedure.*
2. **"Range and meaning: PR interval"** — `cc::topic::cardiovascular::rhythm` · `cc::know::physiology` · `cc::sem::measurement`
3. **"1st-degree AV block recognition"** — `cc::topic::cardiovascular::rhythm` · `cc::know::diagnostics` · `cc::sem::finding`
4. **"STEMI vs NSTEMI mechanism"** — `cc::topic::cardiovascular::coronary` · `cc::know::pathophysiology` · `cc::sem::disorder`
5. **"Which leads show an LAD infarct?"** — `cc::topic::cardiovascular::coronary` · `cc::topic::cardiovascular::rhythm` · `cc::know::diagnostics` · `cc::sem::finding`
   *Two topics (coronary + rhythm/ECG) — polyhierarchy.*
6. **"Management goals for MI"** — `cc::topic::cardiovascular::coronary` · `cc::know::management` · `cc::sem::disorder` · `cc::acuity::emergency`
7. **"Square-wave test: over-damped"** — `cc::topic::cardiovascular::hemodynamics` · `cc::know::diagnostics` · `cc::sem::finding`
8. **"Define preload"** — `cc::topic::cardiovascular::hemodynamics` · `cc::know::physiology` · `cc::sem::concept`
9. **"Hypokalemia ECG changes"** — `cc::topic::cardiovascular::rhythm` · `cc::topic::fluid-electrolyte` · `cc::know::manifestation` · `cc::sem::finding`
10. **"Indication for defibrillation"** — `cc::topic::cardiovascular::rhythm` · `cc::know::management` · `cc::sem::procedure` · `cc::acuity::emergency`
11. **"Treatment for pericarditis"** — `cc::topic::cardiovascular::structural` · `cc::know::management` · `cc::sem::disorder`
12. **"Acute heart failure — what is it?"** — `cc::topic::cardiovascular::failure` · `cc::know::pathophysiology` · `cc::sem::disorder` · `cc::acuity::acute`
13. **"Causes of hypertensive crisis"** — `cc::topic::cardiovascular` · `cc::know::etiology` · `cc::sem::disorder` · `cc::acuity::emergency`
14. **"Pacemaker: fix failure to capture"** — `cc::topic::cardiovascular::rhythm` · `cc::know::management` · `cc::sem::device`
   *No `::pacing` leaf needed — `sem::device` + rhythm + management carries it.*
15. **"What is FiO₂?"** — `cc::topic::respiratory::oxygenation` · `cc::know::physiology` · `cc::sem::concept`
16. **"Non-rebreather mask FiO₂"** — `cc::topic::respiratory::oxygenation` · `cc::know::physiology` · `cc::sem::device`
17. **"Contraindication: nasopharyngeal airway"** — `cc::topic::respiratory::airway` · `cc::know::management` · `cc::sem::device`
18. **"What is PEEP?"** — `cc::topic::respiratory::ventilation` · `cc::know::physiology` · `cc::sem::concept`
19. **"GCS criteria for intubation"** — `cc::topic::respiratory::ventilation` · `cc::know::diagnostics` · `cc::sem::procedure`
20. **"pH criteria for intubation"** — `cc::topic::respiratory::ventilation` · `cc::topic::acid-base` · `cc::know::diagnostics` · `cc::sem::measurement`
21. **"Fast-track extubation steps"** — `cc::topic::respiratory::ventilation` · `cc::know::management` · `cc::sem::procedure`
22. **"What is base excess?"** — `cc::topic::acid-base` · `cc::know::physiology` · `cc::sem::measurement`
23. **"Anion-gap vs non-anion-gap acidosis"** — `cc::topic::acid-base` · `cc::know::pathophysiology` · `cc::sem::disorder`
24. **"Two types of small bowel obstruction"** — `cc::topic::gastrointestinal` · `cc::know::pathophysiology` · `cc::sem::disorder`
25. **"Intervention for DKA"** — `cc::topic::endocrine` · `cc::know::management` · `cc::sem::disorder` · `cc::acuity::emergency`
26. **"Stage 1 AKI criteria"** — `cc::topic::renal` · `cc::know::diagnostics` · `cc::sem::disorder`
27. **"Expected side effects of CPB"** — `cc::topic::perioperative` · `cc::know::complications` · `cc::sem::procedure`
28. **"Coagulation normal values (PLT/INR/aPTT)"** — `cc::topic::hematologic` · `cc::know::physiology` · `cc::sem::measurement`
29. **"Blanchable vs non-blanchable erythema"** — `cc::topic::integumentary` · `cc::know::diagnostics` · `cc::sem::finding`
30. **"Order to draw labs (tube order)"** — `cc::topic::perioperative` · `cc::know::management` · `cc::sem::procedure`
   *Generic nursing skill; no `sys::` gymnastics needed — type+know carry it.*

Every card landed in **3–4 tags** with **no facet deeper than 2 levels**.

---

## How you still study a sub-topic (without a deep tree)

Shallow topics don't lose drill-down — you compose facets in a search/filtered deck:
- All arrhythmia recognition: `tag:cc::topic::cardiovascular::rhythm tag:cc::know::diagnostics`
- All drug mechanisms: `tag:cc::know::physiology tag:cc::sem::drug`
- Everything emergency-management: `tag:cc::know::management tag:cc::acuity::emergency`
- Electrolyte ECG cards: `tag:cc::topic::fluid-electrolyte tag:cc::sem::finding`

Finer named-entity drill-down (e.g. *only* AV-block, *only* amiodarone) is the **deferred
instance-tag layer** (`dx::`/`drug::`) — add later if search proves insufficient (§2.5
pre-coordination), per your "skip for now" decision.

## Honest limitations (carried from the research)

- The disease-schema **order** isn't a validated learning sequence (§1.2) — `know::` is an
  *organizing* axis only.
- The `cause::` sieve facet aids breadth, **not diagnostic accuracy** (§3.2); don't expect
  tagging causes to make reasoning better.
- This only works **if maintained** (§4.5) — hence ~3 tags/card and a planned audit pass.

## Next step

If the facets look right, I'll **map all 258 notes** to v1.0 tags as a reviewable table +
an AnkiConnect apply-script (run locally), then a tag-consistency audit. If anything in the
facet set is off, say so and I'll revise the *system* before mass-tagging.
