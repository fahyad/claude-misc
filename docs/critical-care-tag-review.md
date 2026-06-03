# Critical Care — tag system review (post-application audit)

_Method: every one of the 257 tagged notes was re-read **front AND back** against its
assigned `cc::system::*` / `cc::knowledge::*` tags (the classifier only saw the front). This
is a critical audit — it reports what does **not** fit, not just what does._

## Verdict in one line

The two-axis system **fits the deck well structurally** — every card received a valid
system + knowledge tag, ~2 tags/card, and the large majority are defensible. But reading the
**backs** surfaced four real problems, one of which matters a lot given your goal
(cross-system linking was **under-applied**), plus one clear candidate for a better tag.

## 1. Do all the cards fit? — Yes, with caveats

- **Coverage: 100%.** No card fell through to a `multisystem` fallback; the 12-value system
  vocabulary covered everything. Every card got exactly one knowledge value. The junk
  `"test"` card was correctly excluded.
- **No card was *impossible* to tag.** So the axes are sufficient. The problems below are
  about *accuracy and richness*, not coverage gaps.

## 2. The biggest issue — cross-system tagging was UNDER-applied ⚠️

Your whole reason for this rebuild was that one card can belong to several domains. The
auto-tagger only added a 2nd `system::` when an electrolyte/acid-base **keyword appeared in
the front text**. Cards that span systems via their **back** or clinical context were missed.
Concrete misses found by reading backs:

| Card | Tagged | Should also be | Why |
| --- | --- | --- | --- |
| "Expected side effects of CPB" | `perioperative` | `acid-base` + `fluid-electrolyte` + `hematologic` | Back lists metabolic acidosis, ↓K/Mg/Ca, RBC/platelet destruction |
| "Hemodynamic effect of PPV" | `respiratory` | `cardiovascular` | Card is literally "PPV → ↓cardiac output" |
| "Intervention for DKA" | `endocrine` | `acid-base` + `fluid-electrolyte` | Anion-gap acidosis + K⁺ management are core to the card |
| "PaO₂ / PaCO₂ indication for intubation" | `respiratory` | `acid-base` | ABG values — yet the sibling "pH criteria" card *did* get `acid-base` (inconsistent) |
| "Managment of respiratory arrest" / "…follow-up orders" | `cardiovascular` | `respiratory` | Respiratory-arrest/airway content that only inherited `cardiovascular` from the old CVS subdeck |

**This is the most important finding:** the system *supports* polyhierarchy, but the
mechanical tagging realized it only ~7 times (the electrolyte-ECG cluster). A deliberate
cross-system pass is needed for the system to deliver its main benefit.

## 3. `knowledge::physiology` is overloaded → the only real inconsistency

`physiology` is doing **four** jobs and ended up the largest bucket (93/257, 36%):
1. normal function/concepts (preload, MAP, inotropy)
2. normal values/ranges (CVP, PAWP, lab values)
3. **disease/entity definitions** ("what is ACS / endocarditis / electrical storm")
4. drug mechanism of action

Job #3 is a poor fit — "physiology" implies *normal* function, but it's being used for
disease definitions, and the boundary with `pathophysiology` was applied **inconsistently**:

| "What is [disease]" card | Got |
| --- | --- |
| what is ACS | `physiology` |
| CORONARY ARTERY DISEASE | `pathophysiology` |
| what is endocarditis | `physiology` |
| what is acute heart failure | `pathophysiology` |

These four are the same *kind* of card (define a disease) yet split across two knowledge
values. **This is the clearest defect in the current tagging.**

## 4. A few clear knowledge errors / debatable calls (found via backs)

- **"CRP > 50 indicate?"** → tagged `physiology`; back is "inflammation marker, >50 = bacterial
  infection" = interpreting an abnormal lab → should be **`diagnostics`**. (Clear error.)
- **"Ideal cross-clamp time"** → `physiology` (the <60 min value), but the back is all about
  what *longer* causes (renal/neuro/vent deterioration) → arguably **`complications`** too.
- **"What is an escape beat when fully paced"** → `physiology`, but the back is a failure
  mechanism → closer to `pathophysiology`/`diagnostics`.

Net: knowledge tags are ~95% defensible; ~1 clear error + a handful of judgement calls.
System tags are ~96% defensible once the §2 cross-system misses are fixed.

## 5. The single-knowledge rule strains on multi-fact cards

Some cards bundle two knowledge types, and one tag can't capture both:
- **Nitroglycerin** cloze card = MOA/venodilation (*physiology*) **and** indications
  (*management*) on one note → tagged `management`, losing the MOA facet.
- **"What is acute heart failure"** = definition **and** compensatory mechanism.

This is partly a **card-design** issue (the card mixes facets), not purely a tagging flaw —
but it means the knowledge axis can't always be single-valued. Options: allow a 2nd
knowledge tag for genuinely dual cards, or (better long-term) split such cards.

## 6. Confirmed limitation (known/deferred): no entity gathering

With `sem::`/instance tags dropped, there's no way to pull "all amiodarone cards" — they're
scattered across `physiology` (MOA, electrophysiology) and `management` (admin, prep,
safety, indication). Same for PA-catheter and insulin. This was a deliberate deferral; the
audit confirms it's a real cost for drug-heavy revision, recoverable later via the deferred
`drug::`/`device::` layer.

## What better tags surfaced

1. **`cc::knowledge::definition`** (or rename `physiology` → `concept`) — the strongest
   emergent improvement. Pulls disease/entity definitions out of `physiology` and fixes the
   ACS/CAD/endocarditis/HF inconsistency. `physiology` would then mean *normal function &
   values* only; `definition` = "what is X / overview"; `pathophysiology` = mechanism of
   derangement. Costs one more value but removes the system's biggest ambiguity.
2. **Disciplined cross-system tagging** — not a new facet, but applying the *existing*
   systems to the ~6–10 multi-system cards in §2. This is what makes the rebuild pay off.
3. **(Minor) an infection/ID angle** — CRP, cultures, endocarditis-as-infection have no
   home; they land in `hematologic`/`cardiovascular`. Few cards; `multisystem` or a future
   `system::infectious` could serve, but probably not worth a new value yet.

## Quality scorecard

| Dimension | Assessment |
| --- | --- |
| Coverage (every card fits) | ✅ 100% |
| System tag accuracy | 🟡 ~96% — strong, but cross-system **under-applied** (§2) |
| Knowledge tag accuracy | 🟡 ~95% — 1 clear error, `physiology` overloaded (§3) |
| Consistency | 🟡 disease-definition split (§3); ABG-criteria split (§2) |
| Effort/maintainability | ✅ ~2 tags/card, fast decisions |
| Delivers cross-linking goal | 🔴 only partially — needs the §2 pass |

## Recommended fixes (proposal — nothing changed yet)

1. **Add `cc::knowledge::definition`** and move the "what is [disease/entity]" cards there
   (~10–15 cards), tightening `physiology` to normal-function/values + drug MOA.
2. **Cross-system pass:** add the missing 2nd/3rd `system::` tags to the §2 cards, and fix
   the two respiratory-arrest cards mis-homed under `cardiovascular`.
3. **Fix CRP → `diagnostics`**; re-check the cross-clamp / escape-beat calls.
4. **Decide the dual-knowledge policy:** allow a 2nd `knowledge::` on genuinely dual cards
   (e.g. the nitro card) vs. flag those cards for splitting.
