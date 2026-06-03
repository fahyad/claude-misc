#!/usr/bin/env python3
"""Apply the v1.2 Critical Care tags to your LIVE collection via AnkiConnect.

Run this LOCALLY, on the machine where Anki is open with the AnkiConnect add-on
(code 2055492159) installed. It reads tools/critical_care_tags.json (produced by
tag_critical_care.py) and adds the cc::system::* / cc::knowledge::* tags to each
note by its stable note id.

Safe by design:
  - DRY RUN by default — prints what it would do and changes nothing.
  - Adds tags only; never deletes a card. Re-runnable (addTags is idempotent).
  - --apply actually writes. --reset first strips existing cc::* tags (for redos).

Usage:
  python3 tools/apply_tags_ankiconnect.py            # dry run (preview)
  python3 tools/apply_tags_ankiconnect.py --apply     # apply tags
  python3 tools/apply_tags_ankiconnect.py --apply --reset   # clear cc::* then re-apply

No third-party dependencies (stdlib urllib).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict

ENDPOINT = "http://127.0.0.1:8765"
MAPPING = os.path.join(os.path.dirname(__file__), "critical_care_tags.json")


def invoke(action: str, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ENDPOINT, payload, {"Content-Type": "application/json"})
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=15))
    except urllib.error.URLError as e:
        raise SystemExit(
            f"Could not reach AnkiConnect at {ENDPOINT}. Is Anki open with the "
            f"AnkiConnect add-on installed? ({e})"
        )
    if resp.get("error"):
        raise SystemExit(f"AnkiConnect error on {action}: {resp['error']}")
    return resp["result"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--reset", action="store_true", help="remove existing cc::* tags first")
    args = ap.parse_args()

    with open(MAPPING, encoding="utf-8") as fh:
        mapping = {int(k): v for k, v in json.load(fh).items()}

    ver = invoke("version")
    print(f"Connected to AnkiConnect v{ver}. Notes in mapping: {len(mapping)}")

    # Verify the note ids still exist in the collection.
    found = invoke("notesInfo", notes=list(mapping))
    missing = [nid for nid, info in zip(mapping, found) if not info]
    if missing:
        print(f"⚠️  {len(missing)} note ids not found (skipping): {missing[:5]}…")
    live = [nid for nid, info in zip(mapping, found) if info]

    # Group notes by identical tag-set to minimise calls.
    groups: dict[str, list[int]] = defaultdict(list)
    for nid in live:
        groups[" ".join(mapping[nid])].append(nid)

    print(f"Will tag {len(live)} notes in {len(groups)} tag-group(s).")
    for tagstr, nids in sorted(groups.items()):
        print(f"  [{len(nids):3d}] {tagstr}")

    if not args.apply:
        print("\nDRY RUN — nothing changed. Re-run with --apply to write.")
        return 0

    if args.reset:
        print("\nRemoving existing cc::* tags from these notes…")
        # removeTags strips the given space-separated tags; we pass the union used.
        all_tags = sorted({t for tags in mapping.values() for t in tags})
        invoke("removeTags", notes=live, tags=" ".join(all_tags))

    print("\nApplying…")
    for tagstr, nids in groups.items():
        invoke("addTags", notes=nids, tags=tagstr)
    print(f"Done. Tagged {len(live)} notes.")
    print("Tip: in the Browser, search  tag:cc::*  to review the result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
