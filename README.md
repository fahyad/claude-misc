# Anki deck organization

Tooling to **audit, organize, and clean up** an Anki collection — starting with a
read-only audit so we understand the collection before changing anything.

## Why this approach

This work runs in Claude Code on the web (an isolated cloud container), which
can't reach AnkiConnect on your local machine. So instead of a live API, we work
against an **exported file** you commit to the repo. The audit tool reads it
offline using only the Python standard library — it never writes back to your
collection.

## Workflow

1. **Export** your collection from Anki and drop it in [`decks/`](decks/README.md)
   (full instructions there).
2. **Audit** — generate an inventory + health report:
   ```bash
   python3 tools/anki_audit.py --out audit-report.md
   ```
3. **Decide** what to clean up based on the report (deck restructure, duplicate
   removal, tag fixes — see the report's findings).
4. **Apply** — changes get scripted so you can run them against your live Anki
   (via AnkiConnect) locally, or rebuilt into a new export. (Set up once we've
   reviewed the audit.)

## Layout

| Path | Purpose |
| --- | --- |
| `tools/anki_audit.py` | Read-only auditor for `.colpkg` / `.apkg` / `.anki2`. |
| `decks/` | Where you drop your Anki export. |
| `tests/make_fixture.py` | Builds a synthetic collection to self-test the tools. |

## What the audit reports

- Deck tree with per-deck card counts (total / new / review / suspended / buried)
- Empty decks (removal candidates)
- Note-type usage and field counts
- Tag inventory (top tags by frequency)
- Suspended, buried, and leech counts
- Notes with empty fields and notes with no cards (orphans)
- Likely duplicate notes (same note type + first field, HTML-stripped)
