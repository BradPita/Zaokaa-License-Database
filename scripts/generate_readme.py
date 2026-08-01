#!/usr/bin/env python3
"""
Render the repo-level license data into the README.md table section.

Reads data/licenses_output.csv (one row per tracked/base HF repo) and replaces
everything between <!-- LICENSE_TABLE_START --> and <!-- LICENSE_TABLE_END -->
in README.md. Tracked repos are grouped by model family; base models (used for
derivative tracing) are listed in a separate section. Stdlib only.

Tables are emitted as HTML (not GFM markdown) so that:
  * column widths are fixed and identical across every family table (fixed
    <colgroup> proportions) -> fields line up, easy at-a-glance comparison; and
  * links open in a new tab (target=_blank) instead of navigating away.
"""
from __future__ import annotations

import csv
import html
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

# (header, width, align) - identical proportions for every family table so
# columns line up across tables and stay easy to compare at a glance.
TRACKED_COLS = [
    ("Model", "30%", "left"),
    ("Provider", "9%", "left"),
    ("License", "20%", "left"),
    ("Commercial", "10%", "center"),
    ("Files", "6%", "right"),
    ("Downloads", "8%", "right"),
    ("Updated", "17%", "left"),
]
BASE_COLS = [
    ("Base model", "34%", "left"),
    ("Provider", "12%", "left"),
    ("License", "22%", "left"),
    ("Commercial", "12%", "center"),
    ("Updated", "20%", "left"),
]

# Zero-width space lets long repo/license names wrap instead of stretching a
# column wide (keeps widths consistent across tables).
WBR = "\u200b"


def esc_text(s):
    return html.escape(str(s or "").replace("\n", " ").strip(), quote=False)


def esc_attr(s):
    return html.escape(str(s or "").strip(), quote=True)


def wrappable(s):
    """Insert zero-width break opportunities at separators so long strings wrap."""
    return s.replace("/", "/" + WBR).replace("-", "-" + WBR)


def fmt_date(s):
    s = str(s or "").strip()
    return s[:10] if s else "-"


def fmt_int(s):
    s = str(s or "").strip()
    return format(int(s), ",") if s.isdigit() else "-"


def load_rows():
    if not CSV_FILE.exists():
        return []
    with CSV_FILE.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def anchor(url, text, wrappable_text=False):
    body = wrappable(esc_text(text)) if wrappable_text else esc_text(text)
    return '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>'.format(esc_attr(url), body)


def model_cell(row):
    name = esc_text(row.get("name"))
    hf_id = (row.get("hf_id") or "").strip()
    status = row.get("status", "")
    if status == "ok" and hf_id:
        return anchor("https://huggingface.co/" + hf_id, row.get("name"), wrappable_text=True)
    if status == "not_found":
        return '{} &middot; <em>not found on Hub</em>'.format(name)
    return name


def license_cell(row):
    lic = esc_text(row.get("license")) or "-"
    link_url = (row.get("license_url") or "").strip()
    if lic != "-" and link_url:
        return anchor(link_url, row.get("license"), wrappable_text=True)
    return lic


def html_table(cols, rows):
    out = ["<table>", "<colgroup>"]
    for _, width, _ in cols:
        out.append('<col width="{}">'.format(width))
    out.append("</colgroup>")
    out.extend(["<thead>", "<tr>"])
    for header, _, align in cols:
        out.append('<th align="{}">{}</th>'.format(align, esc_text(header)))
    out.extend(["</tr>", "</thead>", "<tbody>"])
    for cells in rows:
        out.append("<tr>")
        for i, cell in enumerate(cells):
            out.append('<td align="{}">{}</td>'.format(cols[i][2], cell))
        out.append("</tr>")
    out.extend(["</tbody>", "</table>"])
    return out


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
        rows = []
        for r in group:
            comm = esc_text(r.get("commercial_use")) or "Review"
            rows.append([
                model_cell(r), esc_text(r.get("provider")), license_cell(r), comm,
                fmt_int(r.get("file_count")), fmt_int(r.get("downloads")),
                fmt_date(r.get("last_modified")),
            ])
        lines.extend(html_table(TRACKED_COLS, rows))
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
    base_rows.sort(key=lambda r: r.get("name", ""))
    rows = []
    for r in base_rows:
        comm = esc_text(r.get("commercial_use")) or "Review"
        rows.append([
            model_cell(r), esc_text(r.get("provider")), license_cell(r), comm,
            fmt_date(r.get("last_modified")),
        ])
    lines.extend(html_table(BASE_COLS, rows))
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
