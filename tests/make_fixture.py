#!/usr/bin/env python3
"""Build a tiny synthetic Anki-style .apkg to exercise tools/anki_audit.py.

This mimics the legacy (schema 11) collection layout: decks and note types live
as JSON in the ``col`` row, with separate ``notes`` and ``cards`` tables. It is
NOT a real Anki collection -- just enough structure for the auditor to parse.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
import time
import zipfile

FIELD_SEP = "\x1f"


def build_collection(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executescript(
        """
        CREATE TABLE col (id INTEGER PRIMARY KEY, decks TEXT, models TEXT);
        CREATE TABLE notes (id INTEGER PRIMARY KEY, mid INTEGER, tags TEXT, flds TEXT);
        CREATE TABLE cards (id INTEGER PRIMARY KEY, nid INTEGER, did INTEGER,
                            queue INTEGER, type INTEGER);
        """
    )

    decks = {
        "1": {"name": "Default"},
        "100": {"name": "Languages"},
        "101": {"name": "Languages::Spanish"},
        "102": {"name": "Languages::Spanish::Verbs"},
        "103": {"name": "Old Empty Deck"},  # no cards -> should flag as empty
    }
    models = {
        "1000": {"name": "Basic", "flds": [{"name": "Front"}, {"name": "Back"}]},
        "1001": {"name": "Cloze", "flds": [{"name": "Text"}, {"name": "Extra"}]},
    }
    c.execute(
        "INSERT INTO col (id, decks, models) VALUES (1, ?, ?)",
        (json.dumps(decks), json.dumps(models)),
    )

    def note(nid, mid, tags, fields):
        c.execute(
            "INSERT INTO notes (id, mid, tags, flds) VALUES (?, ?, ?, ?)",
            (nid, mid, tags, FIELD_SEP.join(fields)),
        )

    def card(cid, nid, did, queue=0, ctype=0):
        c.execute(
            "INSERT INTO cards (id, nid, did, queue, type) VALUES (?, ?, ?, ?, ?)",
            (cid, nid, did, queue, ctype),
        )

    # Normal notes.
    note(1, 1000, " spanish ", ["hablar", "to speak"])
    card(1, 1, 102, queue=2, ctype=2)  # review
    note(2, 1000, " spanish leech ", ["comer", "to eat"])
    card(2, 2, 102, queue=-1, ctype=2)  # suspended + leech tag
    note(3, 1000, "", ["beber", "to drink"])
    card(3, 3, 101, queue=-3, ctype=2)  # user-buried
    # Duplicate of note 1 (same model + first field) -> should be flagged.
    note(4, 1000, " spanish ", ["Hablar", "to talk (dup)"])
    card(4, 4, 101, queue=0, ctype=0)  # new
    # Empty-field note.
    note(5, 1001, " cloze ", ["{{c1::word}}", ""])
    card(5, 5, 100, queue=0, ctype=0)
    # Orphan note (no card) -> id 6.
    note(6, 1000, "", ["orphan front", "orphan back"])

    conn.commit()
    conn.close()


def main() -> int:
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        "tests", "fixtures", "sample.apkg"
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.TemporaryDirectory() as workdir:
        db = os.path.join(workdir, "collection.anki2")
        build_collection(db)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(db, "collection.anki2")
            zf.writestr("media", json.dumps({}))
    print(f"Wrote fixture: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
