#!/usr/bin/env python3
"""Assign v1.2 (system + knowledge) tags to every Critical Care note.

Reads the exported collection in ./decks, selects notes whose cards live in the
"Critical Care" deck subtree, and assigns:
  - one or more  cc::system::<domain>
  - exactly one  cc::knowledge::<type>

System is derived mostly from the existing deck/tag structure (high confidence);
knowledge is derived from the card's front-field phrasing via ordered rules, with
per-note OVERRIDES for cases the rules get wrong (filled in after review).

Outputs (read-only on the collection -- nothing is written back to Anki):
  - docs/critical-care-tag-mapping.tsv   human-reviewable
  - tools/critical_care_tags.json        {note_id: [tags]} for apply_tags_ankiconnect.py
"""

from __future__ import annotations

import glob
import html
import io
import json
import os
import re
import sqlite3
import tempfile
import zipfile
import zstandard

FIELD_SEP = "\x1f"
TAGRE = re.compile(r"<[^>]+>")

SYSTEMS = [
    "cardiovascular", "respiratory", "renal", "gastrointestinal", "endocrine",
    "neurological", "hematologic", "acid-base", "fluid-electrolyte",
    "integumentary", "perioperative", "multisystem",
]
KNOWLEDGE = [
    "physiology", "etiology", "pathophysiology", "manifestation",
    "diagnostics", "management", "complications",
]

# Junk card ("test", Cloze-table placeholder) — excluded from tagging; recommend deletion.
SKIP_NOTES: set[int] = {1774673713739}

# Per-note corrections applied after manual review of the rule output (all 258 read).
# Built from grouped lists for readability; maps note_id -> {"system"/"knowledge"}.
_KN = {
    "diagnostics": [
        1762540945253, 1762708556539, 1762797719955, 1763108003178, 1763110404568,
        1763118029295, 1763118797033, 1763118797036, 1763122426941, 1763122426944,
        1763122426945, 1763122426946, 1763122426947, 1771311648225, 1777345411226,
        1766721504662, 1772486701095, 1773046533096, 1763403519778, 1763408733289,
        1763408879348, 1763408960499, 1770250941843, 1771346694417, 1763127950412,
    ],
    "management": [
        1763117536742, 1763117764397, 1763121570052, 1763128476010, 1763128737771,
        1763129681648, 1771309634171, 1763395809189, 1763399761554, 1763404727674,
        1765084512840, 1763128822687, 1763405329909, 1765084382244,
    ],
    "pathophysiology": [
        1763106996999, 1764703574736, 1770597143942, 1773046508257, 1763126846007,
        1764703806304,
    ],
    "complications": [1763126717861, 1763394178331],
    # physiology: consistency flips (normal values/definitions) + reviewed-keep
    "physiology": [
        1762704595667, 1763044834099, 1763044855916, 1763093424096, 1765774938512,
        1765777216207, 1771346831835, 1771346910743, 1773431995736, 1763394997541,
        1763395342282, 1765769129313, 1765772635935, 1765772754286, 1765772839234,
        1765779965496, 1771311975151, 1771346470641, 1622234922638, 1769631956348,
        1764505939390, 1771309466855, 1771309725709, 1776397167700, 1763393792330,
        1763393935972, 1763394243404, 1763394369893, 1763394478357, 1763395421512,
        1763396116405, 1763405133540, 1763406546203, 1777112033277, 1765969638804,
        1774678101970,
    ],
}
OVERRIDES: dict[int, dict] = {nid: {"knowledge": kn} for kn, ids in _KN.items() for nid in ids}
# System corrections.
OVERRIDES[1773046578580] = {"system": ["hematologic"], "knowledge": "diagnostics"}  # "Esonophils" misspelled
OVERRIDES[1765970636192] = {"system": ["cardiovascular", "fluid-electrolyte"]}      # Mg effect

# --- v1.3 refinements (from the post-application review) -------------------------
# Rule: a disease/disorder ENTITY (its definition / types / mechanism) -> pathophysiology.
# Normal function/values/concepts and drug MOA stay physiology.
_V13_PATHO = [
    1763107052269,  # what is ACS
    1763107780963,  # 3 types of angina
    1763107871405,  # two types of variant angina
    1762799202178,  # what is a NSVT
    1762710468501,  # what is a premature junctional beat
    1763126556401,  # what is endocarditis
    1772892501171,  # what is electrical storm
    1764504401292,  # two types of small bowel obstruction
    1772305852885,  # escape beat when fully paced (failure mechanism)
]
_V13 = {nid: {"knowledge": "pathophysiology"} for nid in _V13_PATHO}
_V13.update({
    1774931454880: {"knowledge": "diagnostics"},                       # CRP>50 = interpret abnormal lab
    # dual knowledge (cards bundling two knowledge types)
    1776397370945: {"knowledge": ["physiology", "management"]},        # nitroglycerin (MOA + indications)
    1776397431997: {"knowledge": ["physiology", "management"]},        # nitroprusside (MOA + indication)
    1765969638804: {"knowledge": ["physiology", "complications"]},     # ideal cross-clamp time + sequelae
    # cross-system enrichment (polyhierarchy from back content)
    1765969520941: {"system": ["perioperative", "acid-base", "fluid-electrolyte", "hematologic"],
                    "knowledge": "complications"},                     # CPB side effects
    1763401960955: {"system": ["respiratory", "cardiovascular"], "knowledge": "pathophysiology"},  # PPV -> low CO
    1707801865492: {"system": ["endocrine", "fluid-electrolyte", "acid-base"], "knowledge": "management"},  # DKA Rx
    1765083628684: {"system": ["respiratory", "acid-base"], "knowledge": "management"},  # PaO2 criterion
    1765083702340: {"system": ["respiratory", "acid-base"], "knowledge": "management"},  # PaCO2 criterion
    1765084219235: {"system": ["respiratory", "acid-base"], "knowledge": "diagnostics"},  # SAT criteria (pH/lactate)
    1763128362977: {"system": ["respiratory"], "knowledge": "management"},   # mgmt of respiratory arrest
    1763128476010: {"system": ["respiratory"], "knowledge": "management"},   # respiratory arrest follow-up
})
OVERRIDES.update(_V13)


def clean(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\[sound:[^\]]+\]", " ", text)
    text = TAGRE.sub(" ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def load_db(path: str, workdir: str) -> str:
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        if "collection.anki21b" in names:
            data = zstandard.ZstdDecompressor().stream_reader(
                io.BytesIO(zf.read("collection.anki21b"))
            ).read()
            out = os.path.join(workdir, "c.anki2")
            with open(out, "wb") as fh:
                fh.write(data)
            return out
        for cand in ("collection.anki21", "collection.anki2"):
            if cand in names:
                out = os.path.join(workdir, cand)
                with zf.open(cand) as s, open(out, "wb") as d:
                    d.write(s.read())
                return out
    raise SystemExit("no collection db found")


# ---- knowledge classification (ordered; first match wins) -------------------
# Tuned to this deck's actual phrasings (see docs/critical-care-tag-draft-50.md).
KN_RULES: list[tuple[str, str]] = [
    ("complications", r"side effect|complication|adverse|expected.*effect|excessive.*bleed"),
    # pharmacodynamics / mechanism-of-action of a drug or electrolyte -> physiology
    ("physiology", r"\bmoa\b|mechanism of action|physiological effect of|electrophysiology effect"),
    ("management",
     r"managment|management|treatment|interven|indication|administ|\bdose\b|\bprep\b|"
     r"reversal|how to (zero|insert|place|set ?up)|steps? (to|in)|algorith|therapy|"
     r"what to adjust|adjust if|decannulation|weaning|order to draw|removal|safety check|"
     r"set ?up consider|post-resuscitation|targeted temperature|electrical therapy|"
     r"when to stop|goals?|double rate|pre-?intubation"),
    ("manifestation", r"signs? of|symptom|presentation|manifest"),
    ("pathophysiology",
     r"pathophys|physiology of|physiologically|physiological difference|re-entry|"
     r"what occurs in|mechanism (?!of action)|electrical pathway|effect of (positive|mg)|"
     r"what is the physiological|physiologic"),
    ("etiology", r"\bcauses?\b|etiolog|risk factor|precipitat"),
    ("diagnostics",
     r"\becg\b|on ecg|recogni|identif|characteri[sz]|criteria|diagnos|waveform|square wave|"
     r"interval|test to detect|how to calculate|classif|leads?|p-wave|qrs|qtc|"
     r"st (elevation|depression)|damp|thermodilution|\bsvr\b|cardiac index|pawp|\bcvp\b|"
     r"stage 1|staging|what does this|tracing"),
    ("physiology",
     r"what is|what are|define|definition|normal|^range|formula|indicate|purpose of|"
     r"what affects|what remains|relationship between|range and"),
]


def classify_knowledge(front: str) -> tuple[str, bool]:
    f = front.lower()
    for kn, pat in KN_RULES:
        if re.search(pat, f):
            return kn, True
    return "physiology", False  # default + low-confidence flag


# ---- system classification --------------------------------------------------
def classify_systems(deck: str, old_tags: str, text: str) -> list[str]:
    t = text.lower()
    tags = old_tags
    systems: list[str] = []

    def base() -> str:
        if "::CVS" in tags or deck.endswith("CVS"):
            return "cardiovascular"
        if "::Respiratory" in tags or deck.endswith("Respiratory"):
            return "respiratory"
        if deck.endswith("GU") or "::GU" in tags:
            return "renal"
        if deck.endswith("Devices"):
            return "cardiovascular"  # PA cath / pacemaker
        if "Surgery" in deck or "Post_Op" in tags or "::Post" in tags:
            return "perioperative"
        if deck.endswith("Pharmacology"):
            return ""  # decide from content below
        if "GI" in deck or "::GI" in tags:
            return "gastrointestinal"
        return ""

    primary = base()

    # Content-driven overrides / additions (apply regardless of subdeck).
    is_acidbase = re.search(r"\babg\b|anion gap|base excess|acid-?base|acidosis|alkalosis|\bph\b", t)
    is_endocrine = re.search(r"\bdka\b|diabet|insulin|sglt2|glucose|ketone|beta-?hydroxybutyrate|eudka", t)
    is_electrolyte = re.search(r"hypo?kal|hyper?kal|hypo?calc|hyper?calc|magnes|potassium|calcium|electrolyte", t)
    is_heme = re.search(r"coagulation|\bplt\b|\binr\b|\baptt\b|\btxa\b|protamine|fibrinogen|ddavp|"
                        r"\bwbc\b|neutrophil|eosinophil|demargination|platelet|crp", t)
    is_gi = re.search(r"bowel obstruction|small intestine|stomach|ileus|nephrostomy|digestive", t)
    is_integ = re.search(r"erythema|pressure injury|staple|wound", t)

    # Pharmacology subdeck: route by drug content.
    if deck.endswith("Pharmacology"):
        if is_endocrine:
            primary = "endocrine"
        elif is_heme:
            primary = "hematologic"
        else:
            primary = "cardiovascular"  # amiodarone/adenosine/nitro/adrenergic/etc.

    # GI/ABG grab-bag: pick the real domain.
    if "GI" in deck:
        if is_acidbase:
            primary = "acid-base"
        elif is_endocrine:
            primary = "endocrine"
        elif is_gi:
            primary = "gastrointestinal"

    # Surgery grab-bag refinements.
    if "Surgery" in deck:
        if is_heme:
            primary = "hematologic"
        elif is_integ:
            primary = "integumentary"
        else:
            primary = "perioperative"

    if primary:
        systems.append(primary)

    # Cross-system additions (deliberate polyhierarchy).
    if is_electrolyte and "fluid-electrolyte" not in systems:
        systems.append("fluid-electrolyte")
    if is_acidbase and "acid-base" not in systems:
        systems.append("acid-base")
    if is_endocrine and "endocrine" not in systems:
        systems.append("endocrine")

    if not systems:
        systems = ["multisystem"]
    return systems


def main() -> int:
    files = sorted(
        glob.glob("decks/*.colpkg") + glob.glob("decks/*.apkg")
        + glob.glob("decks/*.anki2"),
        key=os.path.getmtime,
    )
    if not files:
        raise SystemExit("no export found in ./decks")
    src = files[-1]

    with tempfile.TemporaryDirectory() as wd:
        db = load_db(src, wd)
        conn = sqlite3.connect(f"file:{os.path.abspath(db)}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        conn.create_collation(
            "unicase", lambda a, b: (a.casefold() > b.casefold()) - (a.casefold() < b.casefold())
        )
        decks = {r["id"]: r["name"].replace("\x1f", "::") for r in conn.execute("SELECT id,name FROM decks")}
        cc_nids: dict[int, str] = {}
        for r in conn.execute("SELECT nid, did FROM cards"):
            nm = decks.get(r["did"], "")
            if nm == "Critical Care" or nm.startswith("Critical Care::"):
                cc_nids.setdefault(r["nid"], nm)
        rows = []
        for r in conn.execute("SELECT id, tags, flds FROM notes"):
            if r["id"] not in cc_nids or r["id"] in SKIP_NOTES:
                continue
            front = clean(r["flds"].split(FIELD_SEP)[0])
            rows.append((r["id"], cc_nids[r["id"]], r["tags"].strip(), front))
        conn.close()

    mapping = {}
    review = []
    tsv = ["note_id\told_deck\tfront\tsystems\tknowledge\tconfidence"]
    from collections import Counter
    kn_dist, sys_dist = Counter(), Counter()
    for nid, deck, old_tags, front in sorted(rows, key=lambda x: x[1]):
        systems = classify_systems(deck, old_tags, front + " " + old_tags)
        knowledge, conf = classify_knowledge(front)
        if nid in OVERRIDES:
            systems = OVERRIDES[nid].get("system", systems)
            knowledge = OVERRIDES[nid].get("knowledge", knowledge)
            conf = True
        kn_list = knowledge if isinstance(knowledge, list) else [knowledge]
        tags = [f"cc::system::{s}" for s in systems] + [f"cc::knowledge::{k}" for k in kn_list]
        mapping[str(nid)] = tags
        for s in systems:
            sys_dist[s] += 1
        for k in kn_list:
            kn_dist[k] += 1
        short_deck = deck.replace("Critical Care::", "") or "(root)"
        tsv.append(f"{nid}\t{short_deck}\t{front[:70]}\t{';'.join(systems)}\t{';'.join(kn_list)}\t{'ok' if conf else 'REVIEW'}")
        if not conf:
            review.append((nid, short_deck, front[:70]))

    os.makedirs("docs", exist_ok=True)
    with open("docs/critical-care-tag-mapping.tsv", "w", encoding="utf-8") as fh:
        fh.write("\n".join(tsv) + "\n")
    with open("tools/critical_care_tags.json", "w", encoding="utf-8") as fh:
        json.dump(mapping, fh, indent=0, sort_keys=True)

    print(f"source: {os.path.basename(src)}")
    print(f"notes tagged: {len(mapping)}")
    print(f"system distribution: {dict(sys_dist)}")
    print(f"knowledge distribution: {dict(kn_dist)}")
    print(f"low-confidence (defaulted) knowledge: {len(review)}")
    for nid, d, f in review:
        print(f"  REVIEW {nid} [{d}] {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
