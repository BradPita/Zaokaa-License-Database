#!/usr/bin/env python3
"""
Generate docs/index.html - the GitHub Pages view of the license table.

GitHub's README sanitizer strips `target="_blank"` and column-width attributes,
so "open in new tab" and "fixed column widths" are impossible inside README.md.
A real HTML page (served by GitHub Pages) has no such restriction: here we use
CSS `table-layout: fixed` for consistent column widths and `target="_blank"`
on every link.

Reads data/licenses_output.csv (one row per repo). Stdlib only.
"""
from __future__ import annotations

import csv
import html
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "licenses_output.csv"
OUT = ROOT / "docs" / "index.html"
PAGES_URL = "https://bradpita.github.io/Zaokaa-License-Database/"

FAMILY_ORDER = [
    "Wan", "FLUX", "Krea", "Qwen-Image", "Qwen-TTS", "Qwen-VL",
    "Qwen3-LLM", "Qwen", "Gemma", "LTX-Video",
    "Z-Image", "Bernini", "SCAIL", "SeedVR", "Segment Anything",
    "LivePortrait", "Pose", "PoseStudio", "Audio", "Anima", "Kaloscope",
]

TRACKED_COLS = [
    ("Model", "30%"), ("Provider", "9%"), ("License", "20%"),
    ("Commercial", "10%"), ("Files", "6%"), ("Downloads", "8%"), ("Updated", "17%"),
]
BASE_COLS = [
    ("Base model", "34%"), ("Provider", "12%"), ("License", "22%"),
    ("Commercial", "12%"), ("Updated", "20%"),
]

COMM_STYLE = {"Yes": "yes", "No": "no", "Review": "rev"}


def esc(s):
    return html.escape(str(s or "").replace("\n", " ").strip(), quote=False)


def esc_attr(s):
    return html.escape(str(s or "").strip(), quote=True)


def fmt_date(s):
    s = str(s or "").strip()
    return s[:10] if s else "-"


def fmt_int(s):
    s = str(s or "").strip()
    return format(int(s), ",") if s.isdigit() else "-"


def link(url, text):
    return '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>'.format(esc_attr(url), esc(text))


def model_cell(r):
    name = esc(r.get("name"))
    hf = (r.get("hf_id") or "").strip()
    st = r.get("status", "")
    if st == "ok" and hf:
        return link("https://huggingface.co/" + hf, r.get("name"))
    if st == "not_found":
        return name + " &middot; <em>not found on Hub</em>"
    return name


def license_cell(r):
    lic = esc(r.get("license")) or "-"
    u = (r.get("license_url") or "").strip()
    if lic != "-" and u:
        return link(u, r.get("license"))
    return lic


def comm_cell(r):
    c = esc(r.get("commercial_use")) or "Review"
    cls = COMM_STYLE.get(c, "rev")
    return '<span class="badge {}">{}</span>'.format(cls, c)


def table(cols, rows):
    out = ['<table><colgroup>']
    for _, w in cols:
        out.append('<col style="width:{}">'.format(w))
    out.append("</colgroup><thead><tr>")
    for h, _ in cols:
        out.append("<th>{}</th>".format(esc(h)))
    out.append("</tr></thead><tbody>")
    for r in rows:
        cells = r
        out.append("<tr>")
        for c in cells:
            out.append("<td>{}</td>".format(c))
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def family_block(tracked):
    parts = []
    by_fam = {}
    for r in tracked:
        by_fam.setdefault(r.get("family", "Other"), []).append(r)
    order = FAMILY_ORDER + sorted(f for f in by_fam if f not in FAMILY_ORDER)
    for fam in order:
        group = by_fam.get(fam)
        if not group:
            continue
        group.sort(key=lambda r: r.get("name", ""))
        parts.append('<section><h3>{}</h3>'.format(esc(fam)))
        rows = []
        for r in group:
            rows.append([
                model_cell(r), esc(r.get("provider")), license_cell(r), comm_cell(r),
                fmt_int(r.get("file_count")), fmt_int(r.get("downloads")), fmt_date(r.get("last_modified")),
            ])
        parts.append(table(TRACKED_COLS, rows))
        parts.append("</section>")
    return "\n".join(parts)


def base_block(base_rows):
    if not base_rows:
        return ""
    base_rows.sort(key=lambda r: r.get("name", ""))
    rows = []
    for r in base_rows:
        rows.append([
            model_cell(r), esc(r.get("provider")), license_cell(r), comm_cell(r),
            fmt_date(r.get("last_modified")),
        ])
    return ('<section><h3 id="base">Base model declarations (for derivative tracing)</h3>'
            '<p class="muted">Original models that derivatives trace up to. Marked per each model\'s own declaration.</p>'
            + table(BASE_COLS, rows) + "</section>")


CSS = """
* { box-sizing: border-box; }
body { font: 14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif; margin: 0; color: #1f2328; background: #f6f8fa; }
.wrap { max-width: 1180px; margin: 0 auto; padding: 24px 20px 60px; }
h1 { font-size: 1.7em; margin: 0 0 .2em; }
h2 { margin-top: 1.8em; border-bottom: 1px solid #d0d7de; padding-bottom: .3em; }
h3 { margin-top: 1.6em; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
.muted { color: #656d76; }
.legend { background: #fff; border: 1px solid #d0d7de; border-radius: 8px; padding: 10px 14px; font-size: 13px; }
.legend b { color: #1f2328; }
table { table-layout: fixed; width: 100%; border-collapse: collapse; background: #fff;
        border: 1px solid #d0d7de; border-radius: 6px; overflow: hidden; margin: 8px 0 18px; }
th, td { padding: 7px 10px; border: 1px solid #eaeef2; text-align: left; vertical-align: top;
         overflow-wrap: anywhere; word-break: break-word; }
th { background: #f6f8fa; font-weight: 650; position: sticky; top: 0; }
td[num], th[align=right], td[align=right] { text-align: right; }
.badge { display: inline-block; padding: 1px 8px; border-radius: 10px; font-size: 12px; font-weight: 600; }
.badge.yes { background: #dafbe1; color: #1a7f37; }
.badge.no  { background: #ffebe9; color: #cf222e; }
.badge.rev { background: #fff8c5; color: #9a6700; }
.src { color: #656d76; font-size: 12px; }
"""


def build_page(rows):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tracked = [r for r in rows if r.get("kind") != "base"]
    base = [r for r in rows if r.get("kind") == "base"]
    with_url = sum(1 for r in tracked if (r.get("license_url") or "").strip())
    body = []
    body.append('<div class="wrap">')
    body.append("<h1>Zaokaa License Database</h1>")
    body.append('<p class="muted">Open-source / open-weight model licenses for the models used by a '
                "ComfyUI-based generation pipeline - license, commercial-use flag, and "
                "derivative-to-base-model tracing.</p>")
    body.append('<p class="muted">Last updated: {} &middot; {} tracked repos + {} base models &middot; {}/{} tracked repos have a license link.</p>'.format(ts, len(tracked), len(base), with_url, len(tracked)))
    body.append('<div class="legend"><b>Commercial:</b> '
                '<span class="badge yes">Yes</span> = usable commercially (permissive, e.g. Apache-2.0/MIT) &nbsp; '
                '<span class="badge no">No</span> = non-commercial (incl. licenses where commercial use must be purchased) &nbsp; '
                '<span class="badge rev">Review</span> = needs human review (other/custom/undeclared). '
                '<b>All links open in a new tab.</b> Fixed column widths for easy comparison.</div>')
    body.append("<h2>Tracked models</h2>")
    body.append(family_block(tracked))
    body.append(base_block(base))
    body.append('<p class="src">Data source: Hugging Face API + <code>data/license_overrides.json</code> '
                "(manual fallbacks + links). Generated by <code>scripts/generate_pages.py</code>.</p>")
    body.append("</div>")
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Zaokaa License Database</title><style>' + CSS + "</style></head><body>"
            + "\n".join(body) + "</body></html>")


def load_rows():
    if not CSV_FILE.exists():
        return []
    with CSV_FILE.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    rows = load_rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_page(rows), encoding="utf-8")
    print("Wrote {} ({} repos). Pages URL: {}".format(OUT, len(rows), PAGES_URL))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
