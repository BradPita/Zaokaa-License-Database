#!/usr/bin/env python3
"""
Render the tracked-model license data into the README.md table section.

Reads data/licenses_output.csv and replaces everything between the
<!-- LICENSE_TABLE_START --> and <!-- LICENSE_TABLE_END --> markers in
README.md. Uses only the Python standard library.
"""
from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "licenses_output.csv"
README = ROOT / "README.md"
START = "<!-- LICENSE_TABLE_START -->"
END = "<!-- LICENSE_TABLE_END -->"

CATEGORY_ORDER = ["image", "video", "llm", "audio"]
CATEGORY_TITLES = {
    "image": "Image Generation",
    "video": "Video Generation",
    "llm": "Large Language Models",
    "audio": "Audio / Music",
}


def esc(s):
    return str(s or "").replace("|", "\\|").replace("\n", " ").strip()


def fmt_date(s):
    s = str(s or "").strip()
    return s[:10] if s else ""


def fmt_downloads(s):
    s = str(s or "").strip()
    return format(int(s), ",") if s.isdigit() else "-"


def load_rows():
    if not CSV_FILE.exists():
        return []
    with CSV_FILE.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def model_cell(row):
    name = esc(row.get("name"))
    hf_id = esc(row.get("hf_id"))
    status = row.get("status", "")
    if status == "ok" and hf_id:
        return "[{}]({})".format(name, "https://huggingface.co/" + hf_id)
    if status == "not_found":
        return "{} · _not found on Hub_".format(name)
    return name


def license_cell(row):
    lic = esc(row.get("license")) or "-"
    link = esc(row.get("license_url"))
    if lic != "-" and link:
        return "[{}]({})".format(lic, link)
    return lic


def build_block(rows):
    lines = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append("_Last updated: {} · {} models tracked_".format(ts, len(rows)))
    lines.append("")

    if not rows:
        lines.append("> _No data yet. Run `python scripts/fetch_licenses.py` "
                     "then `python scripts/generate_readme.py` to populate "
                     "this table (or trigger the GitHub Actions workflow)._")
        return lines

    by_cat = {}
    for r in rows:
        by_cat.setdefault(r.get("category", "other"), []).append(r)
    cats = CATEGORY_ORDER + [c for c in by_cat if c not in CATEGORY_ORDER]

    for cat in cats:
        group = by_cat.get(cat)
        if not group:
            continue
        lines.append("### {}".format(CATEGORY_TITLES.get(cat, cat.title())))
        lines.append("")
        lines.append("| Model | Provider | License | Commercial | Downloads | Updated |")
        lines.append("|---|---|---|---|---|---|")
        for r in group:
            comm = esc(r.get("commercial_use")) or "Review"
            cells = [
                model_cell(r),
                esc(r.get("provider")),
                license_cell(r),
                comm,
                fmt_downloads(r.get("downloads")),
                fmt_date(r.get("last_modified")),
            ]
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    return lines


def main():
    if not README.exists():
        print("README.md not found.", file=sys.stderr)
        return 1
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print("Table markers not found in README.md", file=sys.stderr)
        return 1
    rows = load_rows()
    block = "\n".join(build_block(rows))
    pre = text[:text.index(START) + len(START)]
    post = text[text.index(END):]
    README.write_text(pre + "\n" + block + "\n" + post, encoding="utf-8")
    print("README updated with {} models.".format(len(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
