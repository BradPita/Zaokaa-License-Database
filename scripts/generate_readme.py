#!/usr/bin/env python3
"""
Render the repo-level license data into the README.md table section.

Reads data/licenses_output.csv (one row per tracked/base HF repo) and replaces
everything between <!-- LICENSE_TABLE_START --> and <!-- LICENSE_TABLE_END -->
in README.md. Tracked repos are grouped by model family; base models (used for
derivative tracing) are listed in a separate section. Stdlib only.
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

FAMILY_ORDER = [
    "Wan", "FLUX", "Krea", "Qwen-Image", "Qwen-TTS", "Qwen-VL",
    "Qwen3-LLM", "Qwen", "Gemma", "LTX-Video",
    "Z-Image", "Bernini", "SCAIL", "SeedVR", "Segment Anything",
    "LivePortrait", "Pose", "PoseStudio", "Audio", "Anima", "Kaloscope",
]


def esc(s):
    return str(s or "").replace("|", "\\|").replace("\n", " ").strip()


def fmt_date(s):
    s = str(s or "").strip()
    return s[:10] if s else ""


def fmt_int(s):
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


def family_section(tracked):
    lines = []
    by_fam = {}
    for r in tracked:
        by_fam.setdefault(r.get("family", "Other"), []).append(r)
    order = FAMILY_ORDER + sorted(f for f in by_fam if f not in FAMILY_ORDER)
    for fam in order:
        group = by_fam.get(fam)
        if not group:
            continue
        group.sort(key=lambda r: r.get("name", ""))
        lines.append("### {}".format(fam))
        lines.append("")
        lines.append("| Model | Provider | License | Commercial | Files | Downloads | Updated |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in group:
            comm = esc(r.get("commercial_use")) or "Review"
            cells = [
                model_cell(r), esc(r.get("provider")), license_cell(r), comm,
                fmt_int(r.get("file_count")), fmt_int(r.get("downloads")),
                fmt_date(r.get("last_modified")),
            ]
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    return lines


def base_section(base_rows):
    lines = []
    if not base_rows:
        return lines
    lines.append("### Base model declarations (for derivative tracing)")
    lines.append("")
    lines.append("> Original models that derivatives trace up to. Marked per each model's own declaration.")
    lines.append("")
    lines.append("| Base model | Repo | License | Commercial | Updated |")
    lines.append("|---|---|---|---|---|")
    base_rows.sort(key=lambda r: r.get("name", ""))
    for r in base_rows:
        comm = esc(r.get("commercial_use")) or "Review"
        cells = [model_cell(r), esc(r.get("provider")), license_cell(r), comm, fmt_date(r.get("last_modified"))]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return lines


def build_block(rows):
    lines = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tracked = [r for r in rows if r.get("kind") != "base"]
    base = [r for r in rows if r.get("kind") == "base"]
    lines.append("_Last updated: {} · {} tracked repos + {} base models_".format(ts, len(tracked), len(base)))
    lines.append("")
    if not rows:
        lines.append("> _No data yet. Run `python scripts/fetch_licenses.py` then "
                     "`python scripts/generate_readme.py` (or trigger the GitHub "
                     "Actions workflow) to populate this table._")
        return lines
    lines.append("## Tracked models")
    lines.append("")
    lines.extend(family_section(tracked))
    lines.extend(base_section(base))
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
    print("README updated with {} repos.".format(len(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
