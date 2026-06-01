#!/usr/bin/env python3
"""Read-only auditor for an Anki collection export.

Accepts a full collection (``.colpkg``), a deck export (``.apkg``), or a raw
``collection.anki2`` / ``.anki21`` SQLite file and produces a Markdown report:
deck tree with card-state breakdowns, note-type usage, tag inventory, empty
decks, suspended/buried/leech counts, notes with empty fields, notes with no
cards, and likely duplicate notes.

Nothing is written back to the collection -- the DB is opened read-only on a
temporary copy, so running this can never modify your decks.

Usage:
    python3 tools/anki_audit.py [PATH] [--out report.md]

If PATH is omitted, the newest *.apkg/*.colpkg/*.anki2 under ./decks is used.
"""

from __future__ import annotations

import argparse
import glob
import html
import os
import re
import sqlite3
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

# Field separator inside notes.flds, and the hierarchy separator used by the
# modern (schema >= 15) decks table. The legacy JSON uses "::" instead.
FIELD_SEP = "\x1f"
NEW_DECK_SEP = "\x1f"

# Card "queue" values we care about for cleanup. type: 0=new 1=lrn 2=rev 3=relrn
QUEUE_SUSPENDED = -1
QUEUE_SCHED_BURIED = -2
QUEUE_USER_BURIED = -3

_TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text: str) -> str:
    """Best-effort plain text of an Anki field for comparison/display."""
    text = _TAG_RE.sub(" ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def extract_db(path: str, workdir: str) -> str:
    """Return a filesystem path to a plain SQLite DB for the given input.

    Handles raw .anki2 files and zipped .apkg/.colpkg archives. Modern colpkg
    exports may store the DB zstd-compressed as collection.anki21b; if so and
    the optional 'zstandard' package is unavailable we raise a clear error.
    """
    if not zipfile.is_zipfile(path):
        # Assume it's already a SQLite file.
        return path

    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        # Prefer the newest plain-SQLite member.
        for candidate in ("collection.anki21", "collection.anki2"):
            if candidate in names:
                out = os.path.join(workdir, candidate)
                with zf.open(candidate) as src, open(out, "wb") as dst:
                    dst.write(src.read())
                return out

        if "collection.anki21b" in names:
            raw = os.path.join(workdir, "collection.anki21b")
            with zf.open("collection.anki21b") as src, open(raw, "wb") as dst:
                dst.write(src.read())
            try:
                import zstandard  # type: ignore
            except ImportError as exc:  # pragma: no cover - environment dependent
                raise SystemExit(
                    "This export uses the newer zstd-compressed format "
                    "(collection.anki21b). Either re-export from Anki with "
                    "'Support older Anki versions' checked, or install the "
                    "'zstandard' package (pip install zstandard) and re-run."
                ) from exc
            out = os.path.join(workdir, "collection.anki2")
            with open(raw, "rb") as fh:
                data = zstandard.ZstdDecompressor().decompress(fh.read())
            with open(out, "wb") as fh:
                fh.write(data)
            return out

    raise SystemExit(f"No Anki collection DB found inside {path!r}.")


def connect_readonly(db_path: str) -> sqlite3.Connection:
    uri = f"file:{os.path.abspath(db_path)}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def has_table(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


def load_decks(conn: sqlite3.Connection) -> dict[int, str]:
    """Map deck id -> display name ('::'-separated), across schema versions."""
    decks: dict[int, str] = {}
    if has_table(conn, "decks"):
        for row in conn.execute("SELECT id, name FROM decks"):
            name = row["name"].replace(NEW_DECK_SEP, "::")
            decks[row["id"]] = name
    else:
        import json

        col = conn.execute("SELECT decks FROM col").fetchone()
        for did, deck in json.loads(col["decks"]).items():
            decks[int(did)] = deck["name"]
    return decks


def load_notetypes(conn: sqlite3.Connection) -> dict[int, dict]:
    """Map model id -> {'name': str, 'fields': [str, ...]}."""
    models: dict[int, dict] = {}
    if has_table(conn, "notetypes"):
        for row in conn.execute("SELECT id, name FROM notetypes"):
            models[row["id"]] = {"name": row["name"], "fields": []}
        if has_table(conn, "fields"):
            field_map: dict[int, list[tuple[int, str]]] = defaultdict(list)
            for row in conn.execute("SELECT ntid, ord, name FROM fields"):
                field_map[row["ntid"]].append((row["ord"], row["name"]))
            for ntid, flds in field_map.items():
                if ntid in models:
                    models[ntid]["fields"] = [n for _, n in sorted(flds)]
    else:
        import json

        col = conn.execute("SELECT models FROM col").fetchone()
        for mid, model in json.loads(col["models"]).items():
            models[int(mid)] = {
                "name": model["name"],
                "fields": [f["name"] for f in model.get("flds", [])],
            }
    return models


def audit(db_path: str, source_label: str) -> str:
    conn = connect_readonly(db_path)
    try:
        decks = load_decks(conn)
        models = load_notetypes(conn)

        note_count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        card_count = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]

        # Per-deck card-state breakdown.
        deck_stats: dict[int, Counter] = defaultdict(Counter)
        for row in conn.execute("SELECT did, queue, type FROM cards"):
            s = deck_stats[row["did"]]
            s["total"] += 1
            q = row["queue"]
            if q == QUEUE_SUSPENDED:
                s["suspended"] += 1
            elif q in (QUEUE_SCHED_BURIED, QUEUE_USER_BURIED):
                s["buried"] += 1
            if row["type"] == 0:
                s["new"] += 1
            elif row["type"] == 2:
                s["review"] += 1

        # Note-type usage and tag inventory; collect first fields for dedupe.
        model_usage: Counter = Counter()
        tag_counter: Counter = Counter()
        empty_field_notes = 0
        dup_index: dict[tuple[int, str], list[int]] = defaultdict(list)
        for row in conn.execute("SELECT id, mid, tags, flds FROM notes"):
            model_usage[row["mid"]] += 1
            for tag in row["tags"].split():
                tag_counter[tag] += 1
            fields = row["flds"].split(FIELD_SEP)
            if any(strip_html(f) == "" for f in fields):
                empty_field_notes += 1
            first = strip_html(fields[0]).lower() if fields else ""
            if first:
                dup_index[(row["mid"], first)].append(row["id"])

        notes_with_cards = {
            r["nid"] for r in conn.execute("SELECT DISTINCT nid FROM cards")
        }
        orphan_notes = note_count - len(notes_with_cards)

        leech_notes = sum(c for t, c in tag_counter.items() if t.lower() == "leech")
        used_deck_ids = set(deck_stats)
        empty_decks = [
            decks[d]
            for d in decks
            if d not in used_deck_ids and decks[d].lower() != "default"
        ]
        dup_groups = {k: v for k, v in dup_index.items() if len(v) > 1}
    finally:
        conn.close()

    return render_report(
        source_label=source_label,
        decks=decks,
        models=models,
        note_count=note_count,
        card_count=card_count,
        deck_stats=deck_stats,
        model_usage=model_usage,
        tag_counter=tag_counter,
        empty_field_notes=empty_field_notes,
        orphan_notes=orphan_notes,
        leech_notes=leech_notes,
        empty_decks=empty_decks,
        dup_groups=dup_groups,
    )


def render_report(**ctx) -> str:
    decks: dict[int, str] = ctx["decks"]
    deck_stats: dict[int, Counter] = ctx["deck_stats"]
    models: dict[int, dict] = ctx["models"]
    out: list[str] = []
    w = out.append

    w(f"# Anki collection audit\n")
    w(f"_Source: `{ctx['source_label']}`_\n")

    w("## Summary\n")
    w(f"- **Decks:** {len(decks)} ({len(ctx['empty_decks'])} empty)")
    w(f"- **Note types:** {len(models)}")
    w(f"- **Notes:** {ctx['note_count']:,}")
    w(f"- **Cards:** {ctx['card_count']:,}")
    w(f"- **Unique tags:** {len(ctx['tag_counter'])}")
    susp = sum(s.get("suspended", 0) for s in deck_stats.values())
    bur = sum(s.get("buried", 0) for s in deck_stats.values())
    w(f"- **Suspended cards:** {susp:,}  |  **Buried:** {bur:,}")
    w(f"- **Leech notes:** {ctx['leech_notes']:,}")
    w(f"- **Notes with an empty field:** {ctx['empty_field_notes']:,}")
    w(f"- **Notes with no cards (orphans):** {ctx['orphan_notes']:,}")
    dup_extra = sum(len(v) - 1 for v in ctx["dup_groups"].values())
    w(f"- **Likely duplicate notes:** {len(ctx['dup_groups'])} groups "
      f"({dup_extra:,} redundant)\n")

    w("## Deck tree\n")
    w("| Deck | Cards | New | Review | Suspended | Buried |")
    w("| --- | ---: | ---: | ---: | ---: | ---: |")
    for did in sorted(decks, key=lambda d: decks[d].lower()):
        name = decks[did]
        s = deck_stats.get(did)
        depth = name.count("::")
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * depth
        leaf = name.split("::")[-1]
        if not s:
            w(f"| {indent}{leaf} | 0 | 0 | 0 | 0 | 0 |")
        else:
            w(f"| {indent}{leaf} | {s['total']} | {s['new']} | {s['review']} "
              f"| {s['suspended']} | {s['buried']} |")
    w("")

    if ctx["empty_decks"]:
        w("## Empty decks (candidates to remove)\n")
        for name in sorted(ctx["empty_decks"]):
            w(f"- {name}")
        w("")

    w("## Note-type usage\n")
    w("| Note type | Fields | Notes |")
    w("| --- | ---: | ---: |")
    for mid, count in ctx["model_usage"].most_common():
        m = models.get(mid, {"name": f"<unknown {mid}>", "fields": []})
        w(f"| {m['name']} | {len(m['fields'])} | {count:,} |")
    w("")

    w("## Tags\n")
    if ctx["tag_counter"]:
        w("Top tags by note count:\n")
        for tag, count in ctx["tag_counter"].most_common(30):
            w(f"- `{tag}` — {count:,}")
        if len(ctx["tag_counter"]) > 30:
            w(f"- … and {len(ctx['tag_counter']) - 30} more")
    else:
        w("_No tags in this collection._")
    w("")

    if ctx["dup_groups"]:
        w("## Likely duplicate notes\n")
        w("Notes sharing the same note type and (HTML-stripped) first field. "
          "Review before deleting — some may be intentional.\n")
        shown = 0
        for (mid, first), ids in sorted(
            ctx["dup_groups"].items(), key=lambda kv: -len(kv[1])
        ):
            mname = models.get(mid, {}).get("name", str(mid))
            preview = (first[:80] + "…") if len(first) > 80 else first
            w(f"- **{len(ids)}×** [{mname}] {preview!r} — note ids: "
              f"{', '.join(str(i) for i in ids[:8])}"
              f"{' …' if len(ids) > 8 else ''}")
            shown += 1
            if shown >= 50:
                w(f"- … and {len(ctx['dup_groups']) - 50} more groups")
                break
        w("")

    return "\n".join(out)


def find_default_input() -> str | None:
    candidates: list[str] = []
    for ext in ("*.colpkg", "*.apkg", "*.anki2", "*.anki21"):
        candidates += glob.glob(os.path.join("decks", ext))
        candidates += glob.glob(os.path.join("decks", "**", ext), recursive=True)
    if not candidates:
        return None
    return max(candidates, key=os.path.getmtime)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", help="Path to .colpkg/.apkg/.anki2 export")
    ap.add_argument("--out", help="Write the Markdown report to this file")
    args = ap.parse_args(argv)

    path = args.path or find_default_input()
    if not path:
        print(
            "No input given and nothing found under ./decks.\n"
            "Export your collection from Anki and drop the file in ./decks, "
            "or pass a path explicitly.",
            file=sys.stderr,
        )
        return 2
    if not os.path.exists(path):
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as workdir:
        db_path = extract_db(path, workdir)
        report = audit(db_path, source_label=os.path.basename(path))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"Wrote report to {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
