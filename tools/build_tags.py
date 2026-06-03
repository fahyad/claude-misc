#!/usr/bin/env python3
"""Build the apply-ready tag JSON from the hand-authored mapping.

Source of truth: tools/critical_care_tags_manual.tsv (hand-curated — every Critical
Care note tagged by reading its content, not by classifier rules). This script just
validates that file against the collection and emits:
  - tools/critical_care_tags.json        {note_id: [cc::... tags]}
  - docs/critical-care-tag-mapping.tsv    human-reviewable

Validation (fails loudly):
  - every Critical Care note (minus the known junk card) is present exactly once
  - no unknown note ids
  - every system/knowledge value is in the controlled vocabulary
  - every note has >=1 system and >=1 knowledge tag
"""

from __future__ import annotations

import glob
import io
import json
import os
import sqlite3
import tempfile
import zipfile
import zstandard

MANUAL = os.path.join(os.path.dirname(__file__), "critical_care_tags_manual.tsv")
SKIP_NOTES = {1774673713739}  # junk "test" card

SYSTEMS = {
    "cardiovascular", "respiratory", "renal", "gastrointestinal", "endocrine",
    "neurological", "hematologic", "acid-base", "fluid-electrolyte",
    "integumentary", "perioperative", "multisystem",
}
KNOWLEDGE = {
    "physiology", "etiology", "pathophysiology", "manifestation",
    "diagnostics", "management", "complications",
}


def cc_note_ids() -> set[int]:
    files = sorted(glob.glob("decks/*.colpkg") + glob.glob("decks/*.apkg")
                   + glob.glob("decks/*.anki2"), key=os.path.getmtime)
    if not files:
        raise SystemExit("no export in ./decks")
    with tempfile.TemporaryDirectory() as wd, zipfile.ZipFile(files[-1]) as zf:
        names = set(zf.namelist())
        if "collection.anki21b" in names:
            data = zstandard.ZstdDecompressor().stream_reader(
                io.BytesIO(zf.read("collection.anki21b"))).read()
            db = os.path.join(wd, "c.anki2")
            open(db, "wb").write(data)
        else:
            cand = "collection.anki21" if "collection.anki21" in names else "collection.anki2"
            db = os.path.join(wd, cand)
            open(db, "wb").write(zf.read(cand))
        conn = sqlite3.connect(f"file:{os.path.abspath(db)}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        conn.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold()) - (a.casefold() < b.casefold()))
        decks = {r["id"]: r["name"].replace("\x1f", "::") for r in conn.execute("SELECT id,name FROM decks")}
        ids = set()
        for r in conn.execute("SELECT nid, did FROM cards"):
            nm = decks.get(r["did"], "")
            if nm == "Critical Care" or nm.startswith("Critical Care::"):
                ids.add(r["nid"])
        conn.close()
    return ids


def load_manual() -> dict[int, tuple[list[str], list[str], str]]:
    rows = {}
    with open(MANUAL, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            nid = int(parts[0])
            systems = [s for s in parts[1].split(";") if s]
            knowledge = [k for k in parts[2].split(";") if k]
            front = parts[3] if len(parts) > 3 else ""
            rows[nid] = (systems, knowledge, front)
    return rows


def main() -> int:
    expected = cc_note_ids() - SKIP_NOTES
    manual = load_manual()
    errors = []

    missing = expected - set(manual)
    extra = set(manual) - expected - SKIP_NOTES
    if missing:
        errors.append(f"{len(missing)} notes missing from manual file: {sorted(missing)[:5]}…")
    if extra:
        errors.append(f"{len(extra)} unknown note ids in manual file: {sorted(extra)[:5]}…")
    for nid, (systems, knowledge, _) in manual.items():
        bad_s = [s for s in systems if s not in SYSTEMS]
        bad_k = [k for k in knowledge if k not in KNOWLEDGE]
        if not systems or not knowledge:
            errors.append(f"note {nid}: needs >=1 system and >=1 knowledge")
        if bad_s:
            errors.append(f"note {nid}: bad system value(s) {bad_s}")
        if bad_k:
            errors.append(f"note {nid}: bad knowledge value(s) {bad_k}")
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        return 1

    mapping, tsv = {}, ["note_id\tsystems\tknowledge\tfront"]
    from collections import Counter
    sysd, knd = Counter(), Counter()
    for nid in sorted(manual):
        systems, knowledge, front = manual[nid]
        tags = [f"cc::system::{s}" for s in systems] + [f"cc::knowledge::{k}" for k in knowledge]
        mapping[str(nid)] = tags
        for s in systems:
            sysd[s] += 1
        for k in knowledge:
            knd[k] += 1
        tsv.append(f"{nid}\t{';'.join(systems)}\t{';'.join(knowledge)}\t{front}")

    with open("tools/critical_care_tags.json", "w", encoding="utf-8") as fh:
        json.dump(mapping, fh, indent=0, sort_keys=True)
    with open("docs/critical-care-tag-mapping.tsv", "w", encoding="utf-8") as fh:
        fh.write("\n".join(tsv) + "\n")

    print(f"OK — validated and built {len(mapping)} notes.")
    print(f"system:    {dict(sysd)}")
    print(f"knowledge: {dict(knd)}")
    multi_s = sum(1 for t in mapping.values() if sum('::system::' in x for x in t) > 1)
    multi_k = sum(1 for t in mapping.values() if sum('::knowledge::' in x for x in t) > 1)
    print(f"multi-system notes: {multi_s} | multi-knowledge notes: {multi_k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
