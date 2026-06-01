# Put your Anki export here

Drop your exported Anki file into this folder, then the audit tool will pick up
the newest one automatically.

## How to export from Anki

**Whole collection (recommended for a full audit):**
1. Open Anki on your computer.
2. `File → Export…`
3. Export format: **Anki Collection Package (`.colpkg`)**.
4. **Uncheck "Include media"** (keeps the file small; the audit doesn't need
   images/audio).
5. Tick **"Support older Anki versions"** — this stores the database as plain
   SQLite so the auditor needs no extra dependencies.
6. Save, and move the resulting `.colpkg` into this `decks/` folder.

**A single deck (or subset):**
- Same as above but choose `Anki Deck Package (.apkg)` and pick the deck.
- Include scheduling info if you want suspended/review counts to be meaningful.

## Privacy note

This file contains all your note contents and will be committed to the git
repository on the `claude/anki-deck-organization-3AIu6` branch. Only export what
you're comfortable storing there. If your collection is sensitive, export a
single non-sensitive deck first so we can validate the workflow.

## Run the audit

```bash
python3 tools/anki_audit.py            # uses the newest file in ./decks
python3 tools/anki_audit.py --out audit-report.md
python3 tools/anki_audit.py path/to/specific.colpkg
```
