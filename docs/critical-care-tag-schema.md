# Critical Care — faceted tag schema (DRAFT v0.1)

_Proposal only. No changes have been made to the collection. Grounded in
`medical-knowledge-organization-research.md` and the audit of the 258 notes / 274 cards
currently in the `Critical Care` subdecks._

## Goal

Collapse the 7 subdecks into **one deck (`Critical Care`)** and replace deck-based siloing
with a **small set of orthogonal tag facets**, so a card can live in several topic contexts
at once (e.g. an electrolyte-induced ECG change belongs to *both* cardiology and
electrolytes).

## Design rules (from the research)

| Rule | Why | Source principle |
| --- | --- | --- |
| Few facets, applied consistently | Too many facets → decision paralysis & under-use | Faceting pushback; behavioral reality |
| `::` for hierarchy, **lowercase**, **hyphens** for spaces | Kills synonymy/plural/case drift | Controlled-vocabulary |
| **Singular** nouns (`drug`, not `drugs`) | Avoid plural/singular split | Naming consistency |
| ≤ 3 levels deep per facet | Broad-shallow beats narrow-deep | Depth research |
| Anchor names to standard terms (MeSH/SNOMED-ish) | Borrow, don't invent | Controlled vocabulary |
| One card *may* carry tags from several facets | Deliberate polyhierarchy | SNOMED/MeSH |

> **Naming fix needed:** current tags use `Critical_Care::CVS::ECG::Dysrhythmia`
> (underscore + CamelCase). The target convention is all-lowercase-hyphenated, e.g.
> `sys::cardiovascular::ecg::dysrhythmia`. This remapping is part of migration.

---

## The facets

Two **core** facets are applied to (almost) every card; the rest are **optional**, used
when they add a real retrieval path.

### CORE 1 — `sys::` — system / content area (replaces the subdecks)

The anatomical/clinical topic tree. This is the backbone. Proposed tree for this deck:

```
sys::cardiovascular
sys::cardiovascular::ecg
sys::cardiovascular::ecg::lead-placement
sys::cardiovascular::ecg::intervals          (PR, QRS, QT/QTc, rate calc)
sys::cardiovascular::ecg::morphology          (electrolyte changes, T-wave, ST)
sys::cardiovascular::ecg::dysrhythmia
sys::cardiovascular::ecg::dysrhythmia::sinus
sys::cardiovascular::ecg::dysrhythmia::atrial
sys::cardiovascular::ecg::dysrhythmia::junctional
sys::cardiovascular::ecg::dysrhythmia::ventricular
sys::cardiovascular::ecg::dysrhythmia::av-block
sys::cardiovascular::acs                       (CAD, STEMI/NSTEMI, angina, infarct leads)
sys::cardiovascular::hemodynamics
sys::cardiovascular::hemodynamics::monitoring  (art line, CVP, PA cath, PAWP)
sys::cardiovascular::hemodynamics::principles  (preload, afterload, CO, SV, EF, CI)
sys::cardiovascular::valve-disease
sys::cardiovascular::heart-failure
sys::cardiovascular::pericardium-endocardium   (pericarditis, endocarditis)
sys::cardiovascular::arrest                     (ACLS, defib/cardioversion/pacing, TTM)

sys::respiratory
sys::respiratory::oxygen-delivery               (low-flow / high-flow, FiO2 ranges)
sys::respiratory::airway                        (NPA/OPA/ETT/nasotracheal/trach)
sys::respiratory::niv                           (BiPAP, CPAP, IPAP/EPAP)
sys::respiratory::mech-ventilation              (modes, PEEP, Vt, minute ventilation)
sys::respiratory::intubation                    (criteria, induction agents, ETCO2)
sys::respiratory::weaning                        (SAT, PSV, fast-track extubation)
sys::respiratory::concepts                       (FiO2, shunt/dead space, V/Q)

sys::acid-base                                   (ABG, anion gap, base excess)  ← was buried in GI/ABG
sys::renal                                       (AKI staging, nephrostomy)     ← was GU
sys::gi                                          (anatomy, bowel obstruction)
sys::endocrine::diabetes                         (DKA, EuDKA)                   ← was split GI/Pharm
sys::hematology::coagulation                     (PLT/INR/aPTT, MTP, TXA)       ← was in Surgery
sys::electrolytes                                (K, Ca, Mg)                    ← cross-cuts ECG
sys::perioperative                               (CPB, cross-clamp, staples, post-op bleeding)
```

### CORE 2 — `task::` — clinical task / disease-schema component

What the card teaches you to *do or know* (maps onto the disease-schema components from
the research). Keep this list **short and fixed**:

```
task::physiology            (normal mechanism / values)
task::pathophysiology       (how it goes wrong)
task::assessment            (signs, waveforms, ECG interpretation, monitoring)
task::diagnosis             (criteria, labs, cut-offs, classification)
task::management            (treatment, algorithms, nursing actions)
task::procedure             (how to do/insert/zero/troubleshoot)
task::complication          (risks, expected side effects)
```

### OPTIONAL — `type::` — entity type (when the card is about a discrete thing)

```
type::drug      type::device     type::lab      type::condition
type::equation  type::concept    type::waveform
```

### OPTIONAL — instance gatherers (`drug::`, `device::`) — fix the "scattered entity" problem

High-value recurring entities currently scattered across subdecks. A single instance tag
unifies them regardless of home deck:

```
drug::amiodarone     ← currently MOA / indication / prep / safety in 3 different places
drug::insulin        ← split between GI/ABG and Pharmacology
drug::nitroglycerin  drug::adenosine  drug::epinephrine  drug::atropine ...
device::pa-catheter  ← split between CVS::Hemodynamics and Devices
device::pacemaker    device::art-line  device::ett ...
```

### OPTIONAL — `context::` — acuity / setting

```
context::emergency   (arrest, crisis, peri-arrest)
context::post-op
```

### OPTIONAL — `status::` — personal workflow (not content)

```
status::high-yield   status::weak   status::leech   status::needs-image-fix
```

---

## Worked examples (real cards from your deck)

These show deliberate polyhierarchy — the thing subdecks couldn't do.

| Card (front) | Proposed tags |
| --- | --- |
| "Hypokalemia ECG changes" | `sys::cardiovascular::ecg::morphology` · `sys::electrolytes` · `task::assessment` |
| "Amiodarone MOA" | `sys::cardiovascular::ecg::dysrhythmia` · `drug::amiodarone` · `type::drug` · `task::pathophysiology` |
| "Amiodarone safety check" | `drug::amiodarone` · `type::drug` · `task::management` · `context::emergency` |
| "PA catheter: Right atrial values" | `sys::cardiovascular::hemodynamics::monitoring` · `device::pa-catheter` · `task::assessment` |
| "Intervention for DKA" | `sys::endocrine::diabetes` · `task::management` · `drug::insulin` |
| "Square wave test: over damped" | `sys::cardiovascular::hemodynamics::monitoring` · `device::art-line` · `task::procedure` · `type::waveform` |
| "Indication for defibrillation" | `sys::cardiovascular::arrest` · `task::management` · `context::emergency` |
| "PaO2 indication for intubation" | `sys::respiratory::intubation` · `sys::acid-base` · `task::diagnosis` |

A typical card gets **2–4 tags**: one `sys::`, one `task::`, and optionally a `type::` /
`drug::` / `device::`. That keeps tagging fast (countering the "people under-tag" finding).

---

## Old → new mapping (subdeck → primary `sys::`)

| Current subdeck | Primary new home | Notes |
| --- | --- | --- |
| `Critical Care::CVS` | `sys::cardiovascular::*` | Existing CVS tag tree maps almost 1:1 |
| `Critical Care::Respiratory` | `sys::respiratory::*` | Clean progression already |
| `Critical Care::Devices` | `device::*` + relevant `sys::` | Mostly PA cath / pacemaker — becomes instance tags |
| `Critical Care::GI/ABG` | split: `sys::acid-base`, `sys::gi`, `sys::endocrine::diabetes` | The grab-bag gets un-bundled |
| `Critical Care::GU` | `sys::renal` | Only 2 cards |
| `Critical Care::Pharmacology` | `drug::*` + `type::drug` + `sys::` | Drug-name instance tags unify with CVS drug cards |
| `Critical Care::Surgery/Post-op/Procedures` | `sys::perioperative`, `sys::hematology::coagulation` | |

---

## Suggested rollout (phased, low-risk)

1. **Back up** (full `.colpkg` export) before anything.
2. **Tag, then merge** — apply `sys::` tags *while subdecks still exist* (or use the
   "Convert Subdecks to Tag Hierarchy" add-on `1172858842` to seed them), then move all
   cards into one `Critical Care` deck. Moving cards does not reset scheduling.
3. **Phase 1 — `sys::` only.** Get every card a system tag first; this alone restores
   topic study (via filtered decks / Custom Study by tag).
4. **Phase 2 — `task::`.** Adds the second axis.
5. **Phase 3 — optional facets** (`drug::`, `device::`, `type::`, `status::`) as needed.
6. **Audit pass** — check for duplicate/near-duplicate tags, orphans, naming drift
   (extend `tools/anki_audit.py` with a tag-consistency report).

## Decisions (resolved v0.2)

- **Tag namespace → `cc::` root (Critical-Care-scoped).** All facet tags are prefixed
  with `cc::`, e.g. `cc::sys::cardiovascular::ecg::dysrhythmia::atrial`,
  `cc::task::management`. Self-contained; does not touch other decks. (Trade-off
  acknowledged: not reusable across MCAT/Patho_Pharm — can be promoted to collection-wide
  later by dropping the `cc::` prefix.)
- **Instance tags (`drug::`, `device::`) → deferred.** Drugs/devices are captured via
  `cc::sys::…` + `cc::type::drug`/`type::device` + search, not per-entity tags. Revisit if
  gathering scattered entities (amiodarone, PA catheter) proves painful.

### Still open
- **Granularity of `sys::` leaves** — the tree is a starting point; some leaves
  (e.g. `ecg::intervals`) may merge/split based on how you actually study.
- See `critical-care-tag-draft-50.md` → "Schema adjustments surfaced by this draft" for
  refinements discovered while tagging real cards.
