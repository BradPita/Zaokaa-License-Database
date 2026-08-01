#!/usr/bin/env python3
"""
Fetch license metadata for tracked models from the Hugging Face Hub.

Sources (merged, de-duplicated by repo):
  data/models_manifest.json   - models used by the ComfyUI pipeline (tracked)
  data/extra_models.json      - optional manual additions (same shape)
  data/base_models.json       - original/base models for derivative tracing

Queries the public Hub REST API for each repo's cardData.license and writes
data/licenses_output.csv + .json (one row per repo, with a `kind` column).

License overrides (data/license_overrides.json):
  - fallbacks: when a repackaged repo declares no license, fill it from its
    upstream/original repo (license_source = "fallback:<repo>").
  - links: attach an authoritative license URL (e.g. a GitHub LICENSE) to a
    repo that declares "other" or lacks a usable license_link.
Declared SPDX licenses are never changed.

No external dependencies beyond the Python standard library.
Set HF_TOKEN for a higher rate limit / gated-model metadata (optional).
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "models_manifest.json"
EXTRA = ROOT / "data" / "extra_models.json"
BASE = ROOT / "data" / "base_models.json"
OVERRIDES = ROOT / "data" / "license_overrides.json"
OUT_CSV = ROOT / "data" / "licenses_output.csv"
OUT_JSON = ROOT / "data" / "licenses_output.json"
HF_API = "https://huggingface.co/api/models/{repo_id}"
REQUEST_DELAY = 1.0
TIMEOUT = 30

PERMISSIVE = {
    "apache-2.0", "mit", "bsd-2-clause", "bsd-3-clause", "mpl-2.0",
    "isc", "unlicense", "cc0-1.0", "zlib",
}
NC_MARKERS = (
    "non-commercial", "noncommercial", "non_commercial",
    "cc-by-nc", "nc-sa", "nc-nd",
    "fair-ai-public-license", "faipl",
)

# Authoritative SPDX license page for well-known standard licenses, used to give
# every such model a clickable license link when the repo provides none.
SPDX_URLS = {
    "apache-2.0": "https://spdx.org/licenses/Apache-2.0.html",
    "mit": "https://spdx.org/licenses/MIT.html",
    "bsd-2-clause": "https://spdx.org/licenses/BSD-2-Clause.html",
    "bsd-3-clause": "https://spdx.org/licenses/BSD-3-Clause.html",
    "mpl-2.0": "https://spdx.org/licenses/MPL-2.0.html",
    "isc": "https://spdx.org/licenses/ISC.html",
    "unlicense": "https://spdx.org/licenses/Unlicense.html",
    "cc0-1.0": "https://spdx.org/licenses/CC0-1.0.html",
    "cc-by-4.0": "https://spdx.org/licenses/CC-BY-4.0.html",
    "cc-by-sa-4.0": "https://spdx.org/licenses/CC-BY-SA-4.0.html",
    "cc-by-nc-4.0": "https://spdx.org/licenses/CC-BY-NC-4.0.html",
    "cc-by-nc-sa-4.0": "https://spdx.org/licenses/CC-BY-NC-SA-4.0.html",
}

FAMILY_RULES = [
    ("wan2", "Wan"), ("wan", "Wan"), ("wanvideo", "Wan"),
    ("krea", "Krea"), ("flux", "FLUX"),
    ("qwen3-tts", "Qwen-TTS"), ("qwen-tts", "Qwen-TTS"),
    ("qwen-image", "Qwen-Image"), ("qwen_image", "Qwen-Image"),
    ("qwenedit", "Qwen-Image"),
    ("qwen2.5-vl", "Qwen-VL"), ("qwen3", "Qwen3-LLM"), ("qwen", "Qwen"),
    ("gemma", "Gemma"), ("ltx", "LTX-Video"),
    ("z_image", "Z-Image"), ("z-image", "Z-Image"),
    ("bernini", "Bernini"), ("scail", "SCAIL"),
    ("seedvr", "SeedVR"), ("sam", "Segment Anything"),
    ("liveportrait", "LivePortrait"),
    ("dwpose", "Pose"), ("vitpose", "Pose"), ("sdpose", "Pose"),
    ("posestudio", "PoseStudio"),
    ("melbandroformer", "Audio"), ("wav2vec2", "Audio"),
    ("hunyuan_foley", "Audio"), ("audio", "Audio"),
    ("anima", "Anima"), ("kaloscope", "Kaloscope"),
]

CSV_FIELDS = [
    "name", "provider", "family", "kind", "categories", "hf_id",
    "file_count", "license", "license_url", "license_source",
    "commercial_use", "downloads", "likes", "pipeline_tag",
    "last_modified", "status",
]


def family_of(repo):
    s = repo.lower()
    for kw, fam in FAMILY_RULES:
        if kw in s:
            return fam
    return repo.split("/")[0]


def load_overrides():
    if not OVERRIDES.exists():
        return {}, {}
    data = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    fallbacks = {fb["repo"]: fb for fb in data.get("fallbacks", [])}
    links = {lk["repo"]: lk for lk in data.get("links", [])}
    return fallbacks, links


def load_repos():
    """Return {repo: {'kind','categories':set,'files':int}} merged from sources."""
    repos = {}

    def add(repo, kind, category):
        if not repo:
            return
        r = repos.setdefault(repo, {"kind": kind, "categories": set(), "files": 0})
        if kind == "tracked":
            r["kind"] = "tracked"
        r["files"] += 1
        if category:
            r["categories"].add(category)

    if MANIFEST.exists():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for f in data.get("files", []):
            add(f.get("hf_repo", ""), "tracked", f.get("category", ""))
    if EXTRA.exists():
        data = json.loads(EXTRA.read_text(encoding="utf-8"))
        for f in data.get("files", []):
            add(f.get("hf_repo", ""), "tracked", f.get("category", ""))
    if BASE.exists():
        data = json.loads(BASE.read_text(encoding="utf-8"))
        for b in data.get("bases", []):
            add(b.get("hf_repo", ""), "base", "")
    return repos


def hf_request(repo_id):
    url = HF_API.format(repo_id=repo_id)
    headers = {"User-Agent": "Zaokaa-License-Database/1.0"}
    token = os.environ.get("HF_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print("  ! HTTP {} for {}: {}".format(e.code, repo_id, e.reason), file=sys.stderr)
        return None
    except Exception as e:
        print("  ! Error for {}: {}".format(repo_id, e), file=sys.stderr)
        return None


def assess_commercial(license_value):
    if not license_value:
        return "Review"
    s = license_value.lower()
    if any(m in s for m in NC_MARKERS):
        return "No"
    if any(p in s for p in PERMISSIVE):
        return "Yes"
    return "Review"


def parse_license(card_data):
    if not card_data:
        return "", ""
    lic = card_data.get("license")
    if isinstance(lic, list):
        lic = ", ".join(str(x) for x in lic if x)
    elif lic is not None:
        lic = str(lic)
    else:
        lic = ""
    link = card_data.get("license_link") or card_data.get("license_name") or ""
    return lic.strip(), (link or "").strip()


def fetch_one(repo, meta, fallbacks, links):
    row = {k: "" for k in CSV_FIELDS}
    row["name"] = repo
    row["provider"] = repo.split("/")[0]
    row["family"] = family_of(repo)
    row["kind"] = meta["kind"]
    row["categories"] = ", ".join(sorted(meta["categories"]))
    row["hf_id"] = repo
    row["file_count"] = meta["files"]
    row["status"] = "pending"

    info = hf_request(repo)
    if info is None:
        row["status"] = "not_found"
        return row

    card = info.get("cardData") or {}
    lic, link_url = parse_license(card)
    source = "cardata"
    commercial = ""

    if not lic and repo in fallbacks:
        fb = fallbacks[repo]
        lic = fb.get("license", "")
        commercial = fb.get("commercial_use", "")
        src = fb.get("source_repo", "")
        link_url = "https://huggingface.co/" + src if src else ""
        source = "fallback:" + src
    else:
        commercial = assess_commercial(lic)

    if repo in links:
        link_url = links[repo].get("license_url", "")
        source = source + "+link" if source != "cardata" else "cardata+link"

    if not link_url and lic:
        spdx = SPDX_URLS.get(lic.lower().split(",")[0].strip())
        if spdx:
            link_url = spdx
            source = "spdx" if source == "cardata" else source + "+spdx"

    row["license"] = lic
    row["license_url"] = link_url
    row["license_source"] = source
    row["commercial_use"] = commercial or assess_commercial(lic)
    row["downloads"] = info.get("downloads", "")
    row["likes"] = info.get("likes", "")
    row["pipeline_tag"] = info.get("pipeline_tag") or ""
    row["last_modified"] = info.get("lastModified") or ""
    row["status"] = "ok"
    return row


def main():
    repos = load_repos()
    if not repos:
        print("No repos found. Run extract_manifest.py first.", file=sys.stderr)
        return 1
    fallbacks, links = load_overrides()
    print("Tracking {} repos ({} fallbacks, {} links)".format(len(repos), len(fallbacks), len(links)))
    rows = []
    for i, (repo, meta) in enumerate(sorted(repos.items()), 1):
        print("[{}/{}] ({}) {}".format(i, len(repos), meta["kind"], repo))
        rows.append(fetch_one(repo, meta, fallbacks, links))
        if i < len(repos):
            time.sleep(REQUEST_DELAY)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_count": len(rows),
        "models": rows,
    }
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    ok = sum(1 for r in rows if r["status"] == "ok")
    nf = sum(1 for r in rows if r["status"] == "not_found")
    fb_used = sum(1 for r in rows if r["license_source"].startswith("fallback"))
    link_used = sum(1 for r in rows if "link" in r["license_source"])
    print("Done. ok={} not_found={} fallback={} link={}".format(ok, nf, fb_used, link_used))
    return 0


if __name__ == "__main__":
    sys.exit(main())
