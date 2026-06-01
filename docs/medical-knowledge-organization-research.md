# Organizing medical knowledge — research foundation

_Research compiled 2026-06-01 to inform the design of a faceted tagging system for
medical study material. Scope (chosen by user): cognitive/educational frameworks,
formal terminologies/ontologies, and differential-diagnosis frameworks. Role-agnostic
(nursing + physician)._

## How to read this

Each framework is presented as **claim → usefulness → pushback**, because the goal was
an explicitly *balanced* base: every significant claim was paired with counter-evidence
or a stated limitation. Confidence ratings reflect cross-source corroboration and the
strength of the pushback.

### ⚠️ Evidence-grade caveat (read before quoting figures)

This research was run through a fan-out of web-search agents. **Full-text page fetching
was blocked (HTTP 403) in the execution environment**, so specific numeric figures
(effect sizes, the 26% post-coordination error rate, Script Concordance Test scores)
come from **search-engine extracts of real journal/standards URLs, not full-text reads.**
Treat those numbers as "as reported by the search index" and confirm against primary text
before citing authoritatively. Structural/qualitative claims corroborated by two or more
independent angles are noted as such and are higher-confidence.

---

## The one finding that matters most

Across all lenses there is a recurring tension worth stating up front:

> **The structures that look best on paper — rich tags, facets, multi-classification —
> are systematically _under-used_ in real personal practice.** When given both folders and
> tags, people prefer folders and rarely apply more than a single tag per item; multi-
> classification is "exceptional" even among users who believe it's a good idea
> (Civan/Jones/Klasnja/Bruce, ASIST 2008; Bergman 2013).

So the design problem is as much **behavioral** (will I maintain it?) as **logical**
(is it well-structured?). Every principle below is filtered through that lens.

---

## Lens 1 — Cognitive/educational frameworks

### 1.1 Illness scripts & knowledge encapsulation — _Confidence: high_
**Claim.** As expertise grows, detailed pathophysiology becomes "encapsulated" under
higher-order clinical concepts, stored as *illness scripts* (enabling conditions → fault/
pathophysiology → consequences) that activate as a unit.
- Support: [Schmidt & Boshuizen, Med Educ 2007](https://pubmed.ncbi.nlm.nih.gov/18004989/);
  [clinicalreasoning.org](https://clinicalreasoning.org/illness-scripts/)
- **Pushback.** The empirical signature (the "intermediate effect") has **failed to
  replicate** in some studies ([PMID 10753544](https://pubmed.ncbi.nlm.nih.gov/10753544/)).
  Critically, the *same* pattern-matching machinery is a documented **source of diagnostic
  error** — premature closure, anchoring, representativeness
  ([AHRQ PSNet](https://psnet.ahrq.gov/web-mm/anchoring-bias-critical-implications);
  [Merck Manual](https://www.merckmanuals.com/professional/special-subjects/clinical-decision-making/cognitive-errors-in-clinical-decision-making)).

### 1.2 The standard disease schema — _Evidence thin_
**Claim.** The template *etiology → pathophysiology → epidemiology → clinical features →
investigations → management → complications* maps onto illness-script components.
- Support: [Diagnostic Schemas, PMC9905354](https://pmc.ncbi.nlm.nih.gov/articles/PMC9905354/);
  [StatPearls NBK543763](https://www.ncbi.nlm.nih.gov/books/NBK543763/box/ch1.FPar1/)
- **Pushback.** This is a **convention, not a validated sequence** — no controlled
  evidence that this exact ordering beats alternatives for learning. Treat as scaffolding.

### 1.3 Semantic qualifiers — _Confidence: high (recall); contested (accuracy)_
**Claim.** Recasting findings as paired abstractions (acute/chronic, proximal/distal)
improves recall and organization of a case.
- Support: [clinicalreasoning.org](https://clinicalreasoning.org/problem-representation/)
- **Pushback.** Nendaz & Bordage: students recalled cases better **but did not diagnose
  more accurately** ([StatPearls NBK543761](https://www.ncbi.nlm.nih.gov/books/NBK543761/)).
  A 2025 RCT found an accuracy benefit only when qualifiers were *appropriate* **and**
  combined with decision support
  ([BMC Med Educ 2025](https://link.springer.com/article/10.1186/s12909-025-07294-5)) —
  conditional, not intrinsic.

### 1.4 Teaching scripts/schemas — _Confidence: moderate_
**Claim.** Explicit illness-script instruction improves reasoning scores
([RCT, PMC7856771](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7856771/)).
- **Pushback.** (a) **Expertise-reversal effect** — step-by-step scaffolding that helps
  novices *hinders* advanced learners via redundant load
  ([Wikipedia](https://en.wikipedia.org/wiki/Expertise_reversal_effect);
  [PMID 21443379](https://pubmed.ncbi.nlm.nih.gov/21443379/)). (b) Outcome circularity —
  gains often measured with the Script Concordance Test, whose validity is itself disputed
  ([validity-threats paper](https://www.researchgate.net/publication/258425168)).

### 1.5 Concept maps / mind maps — _Confidence: low–moderate_
**Claim.** Concept maps improve integration and sometimes scores
([2025 review](https://link.springer.com/article/10.1007/s10459-025-10437-4);
[BEME Guide 81](https://www.tandfonline.com/doi/full/10.1080/0142159X.2023.2281248)).
- **Pushback.** Inconsistent — many studies find **no performance difference, only that
  students prefer maps**; small samples
  ([Daley & Torre](https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/j.1365-2923.2010.03628.x)).
  Collaborative mapping degrades into "node-dumping"
  ([JMIR Med Educ 2025](https://mededu.jmir.org/2025/1/e57331)).

### 1.6 Dual coding (verbal + visual) — _Confidence: high, with boundary conditions_
**Claim.** Pairing words and images strengthens encoding (the Sketchy/Physeo rationale)
([dual-coding theory](https://en.wikipedia.org/wiki/Dual-coding_theory)).
- **Pushback.** Benefit holds **only when image and text converge and are integrated**;
  when redundant or split, the combination *increases* load and **harms** learning
  ([Kalyuga et al. 1999](https://onlinelibrary.wiley.com/doi/abs/10.1002/(SICI)1099-0720(199908)13:4%3C351::AID-ACP589%3E3.0.CO;2-6);
  [Frontiers 2023](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1148035/full)).
  Frequently conflated with the debunked "learning styles" myth
  ([Science-Based Medicine](https://sciencebasedmedicine.org/brain-based-learning-myth-versus-reality-testing-learning-styles-and-dual-coding/)).

---

## Lens 2 — Formal terminologies/ontologies (the borrowable structure)

_The most structurally instructive lens. Claims corroborated across two independent
research angles._

### 2.1 Polyhierarchy — _Confidence: high_
**Claim.** A concept can have multiple parents (a DAG, not a tree); SNOMED CT and MeSH
are built this way — the formal answer to "one card, many topics."
- Support: [SNOMED glossary](https://docs.snomed.org/snomed-international-documents/snomed-ct-glossary/p/polyhierarchy);
  [MeSH trees](https://www.nlm.nih.gov/mesh/intro_trees.html)
- **Pushback.** Too many parents **raises cognitive load and navigation cost**; weak
  multi-parent links are better modeled as "see also" than true *is-a*
  ([Synaptica](https://synaptica.com/on-polyhierarchy/)).

### 2.2 Faceted / multi-axial classification — _Confidence: high_
**Claim.** Describe an item by several **orthogonal axes** rather than one node. LOINC
names every lab test by 6 axes; Ranganathan's PMEST is the origin.
- Support: [LOINC structure](https://loinc.org/kb/faq/structure/);
  [PMEST](https://www.lisedunetwork.com/ranganathans-pmest-the-foundation-of-faceted-classification/)
- **Pushback.** Faceting **silently permits nonsensical combinations** (ICD-11 axes
  "allow invalid combinations,"
  [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1386505625000383))
  and "too many facets cause decision paralysis"
  ([Faceted classification](https://grokipedia.com/page/Faceted_classification)).

### 2.3 Separate concept from words (controlled vocab + synonyms) — _Confidence: high_
**Claim.** One stable ID owns many synonyms (SNOMED Concept vs Description; UMLS CUI).
- Support: [SNOMED logical model](https://docs.snomed.org/snomed-ct-practical-guides/snomed-ct-starter-guide/5-snomed-ct-logical-model);
  [UMLS glossary](https://www.nlm.nih.gov/research/umls/new_users/glossary.html)
- **Pushback.** Deciding synonymy is **error-prone at scale** — UMLS has documented
  "wrong synonymy" errors ([PMC4303374](https://pmc.ncbi.nlm.nih.gov/articles/PMC4303374/)).

### 2.4 A small top-level "semantic type" layer — _Confidence: moderate–high_
**Claim.** A handful of broad types over fine-grained concepts gives reliable roll-up
(UMLS overlays ~135 semantic types on 2M+ concepts)
([UMLS Semantic Network](https://uts.nlm.nih.gov/uts/umls/semantic-network)).
- **Pushback.** Type assignment by many editors becomes **inconsistent and self-
  contradictory** ([PMC6537875](https://pmc.ncbi.nlm.nih.gov/articles/PMC6537875/)).

### 2.5 Pre- vs post-coordination — _Confidence: moderate (snippet-sourced figure)_
**Claim.** Use ready-made tags for common things; compose atomic tags only for rare
combinations
([SNOMED post-coordination](https://docs.snomed.org/snomed-ct-practical-guides/snomed-ct-postcoordination-guide/snomed-ct-expressions/precoordination-and-postcoordination)).
- **Pushback.** Composition lets the same meaning be encoded multiple non-equal ways —
  a study reported a **~26% error rate**, cut to 2% only with strict canonical-form rules
  ([PMC2949694](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2949694/)). Lesson: if you
  compose tags, fix **one canonical order**.

### 2.6 Scale makes inconsistency inevitable → audit is structural — _Confidence: high (under-challenged)_
**Claim.** Large terminologies are big enough that "errors are all but inevitable,"
making auditing structural, not optional
([PMC8363812](https://pmc.ncbi.nlm.nih.gov/articles/PMC8363812/); ~30% of audited SNOMED
groups had ≥1 inconsistency, [PMC5835197](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5835197/)).
- **Pushback.** Thin — near-consensus; caveat is that audits flag *possible* issues only.

---

## Lens 3 — Differential-diagnosis "sieve" frameworks

### 3.1 The surgical sieve / VINDICATE / VITAMIN-CDEF — _Confidence: high_
**Claim.** Force consideration of a fixed set of etiological buckets against any
presentation
([Surgical sieve](https://en.wikipedia.org/wiki/Surgical_sieve);
[Geeky Medics](https://geekymedics.com/medical-mnemonics/)).
- **Pushback.** **Proliferation of competing "universal" mnemonics** (VINDICATE-P,
  VITAMIN-CDEF, KITTENS, ATOMIC-DDT…) shows none is authoritative and letter-fitting is
  arbitrary ([PMC4853007](https://pmc.ncbi.nlm.nih.gov/articles/PMC4853007/)). A sieve is
  a **categorical aid, not a reasoning method** — it doesn't prioritize by likelihood
  ([doctorodonovan](https://www.doctorodonovan.com/videos/surgical-differential-guide)).

### 3.2 The key empirical through-line — _Confidence: high_
Sieves/mnemonics reliably **increase the number of differentials**
([Chai et al., Clinical Teacher 2017](https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/tct.12546))
**but more differentials ≠ better accuracy**
([systematic review PMC8390726](https://pmc.ncbi.nlm.nih.gov/articles/PMC8390726/)).

### 3.3 Cognitive-forcing / debiasing — _Confidence: high_
**Claim.** Systematic reasoning protects against premature closure
([Merck Manual](https://www.merckmanuals.com/professional/special-subjects/clinical-decision-making/cognitive-errors-in-clinical-decision-making)).
- **Pushback (direct).** A controlled trial of 191 students —
  **"Ineffectiveness of cognitive forcing strategies"** — found no reduction in diagnostic
  error ([Sherbino et al. 2014, CJEM](https://pubmed.ncbi.nlm.nih.gov/24423999/)); System-2
  is *also* prone to confirmation bias
  ([PMC10702679](https://pmc.ncbi.nlm.nih.gov/articles/PMC10702679/)).

### 3.4 Anatomical & physiological sieves — _Evidence thin both ways_
Advocated alternatives ("the heart is a house",
[SAGE 2021](https://journals.sagepub.com/doi/10.1177/23821205211035235)) but **no trial
shows superiority over etiological sieves on accuracy.** Consensus pedagogy, untested.

---

## Lens 4 — Knowledge-organization structure (the design layer)

### 4.1 Three complementary paradigms — _Confidence: high_
Hierarchy (one place, navigable, can't represent overlap) · facets (combine orthogonal
axes on demand) · network/Zettelkasten (explicit links)
([Faceted classification](https://en.wikipedia.org/wiki/Faceted_classification)).
- **Pushback per paradigm.** Hierarchies are "rigid"; facets need "high intellectual
  effort" and risk "decision paralysis"; networks create "cognitive overhead" and
  "mindless linking" ([Zettelkasten forum](https://forum.zettelkasten.de/discussion/2592/)).

### 4.2 Classification (one place) vs indexing/tagging (many places) — _Confidence: high (LIS consensus)_
Complementary, not interchangeable: store once, tag for many access points
([LIS: index vs classification](https://www.lisedunetwork.com/index-vs-library-classification/)).
Robust pattern = **shallow hierarchy + tag/network layer**.

### 4.3 Naming consistency — _Confidence: high_
Uncontrolled tags drift via synonymy, polysemy, plurals, granularity
([Webology](https://www.webology.org/2007/v4n2/editorial12.html)).
- **Counter-evidence.** Stable shared vocabularies can **emerge even without central
  control** ([Folksonomy](https://en.wikipedia.org/wiki/Folksonomy)) — but in medicine a
  controlled vocabulary measurably improves retrieval
  ([JMIR Med Inform 2023](https://medinform.jmir.org/2023/1/e43750/)).

### 4.4 Depth: broad-shallow beats narrow-deep — _Confidence: moderate–high_
Perceived complexity rises with depth; a "concave" shape (broad top, narrow middle,
broad leaves) is optimal
([Human Factors](https://www.humanfactors.com/newsletters/breadth_vs_depth_we_revisit_this_question.asp);
[UMD HCIL](https://www.cs.umd.edu/hcil/trs/99-15/99-15.html)).
- **Pushback.** Context-dependent (screen-reader / in-vehicle UIs shift the trade-off).

### 4.5 ⚠️ The behavioral reality check — _Confidence: high_
Given both folders and tags, people **prefer folders and rarely apply more than a single
tag per item** — multi-classification is "exceptional" even among believers
([Civan et al., JASIST](https://onlinelibrary.wiley.com/doi/abs/10.1002/asi.22906)).
- **Counter.** May reflect habit/tooling; taught users can shift
  ([Academia.edu](https://www.academia.edu/59576791/)).
- **Implication.** The multi-tag freedom only pays off **if maintained** — otherwise the
  tag layer silently rots.

---

## Design principles that survive their own pushback

These are the transferable conclusions used to build the tag schema
(see `critical-care-tag-schema.md`):

1. **Faceted, not one deep tree.** A *small fixed set of orthogonal axes*
   (System · Task · Entity-type · …). Dissolves siloing. _Guardrail: few facets; watch
   for invalid combinations._
2. **Exploit polyhierarchy deliberately.** One card under multiple parents is legitimate
   (SNOMED/MeSH do it) — but distinguish true *is-a* from "related-to".
3. **Borrow a controlled vocabulary; don't invent one.** Anchor names to MeSH/SNOMED
   preferred terms; keep a short synonym list. Fixes synonymy/plural drift.
4. **Pick one canonical granularity and stop.** Over-specific tags fragment retrieval;
   if you compose, fix one canonical form.
5. **Keep it broad-and-shallow** (≤2–3 levels per facet).
6. **Budget for entropy.** Inconsistency is inevitable and people under-tag — schedule
   periodic tag-merge/audit passes.

### Honest limits to carry forward
- Disease schemas and sieves are useful **organizing scaffolds** but are **not proven to
  make you reason or diagnose better** (number ≠ accuracy; cognitive-forcing failed a
  controlled trial).
- Rigid templates help novices but can **hinder experts** (expertise reversal).
- The richest tagging structure only works **if you actually maintain it.**
