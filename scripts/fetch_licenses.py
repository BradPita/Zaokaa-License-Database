#!/usr/bin/env python3
"""
Fetch license metadata for tracked models from the Hugging Face Hub.

Uses the public Hub REST API (https://huggingface.co/api/models/{repo_id}).
No external dependencies beyond the Python standard library.

Set the HF_TOKEN environment variable for a higher rate limit and access to
gated-model metadata (optional - public license metadata does not require it).
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
TRACK_FILE = ROOT / "data" / "models_to_track.json"
OUT_CSV = ROOT / "data" / "licenses_output.csv"
OUT_JSON = ROOT / "data" / "licenses_output.json"
HF_API = "https://huggingface.co/api/models/{repo_id}"
REQUEST_DELAY = 1.0
TIMEOUT = 30

# SPDX identifiers unambiguously permissive for commercial use.
PERMISSIVE = {
    "apache-2.0", "mit", "bsd-2-clause", "bsd-3-clause", "mpl-2.0",
    "isc", "unlicense", "cc0-1.0", "zlib",
}
# Substrings that signal a non-commercial restriction.
NC_MARKERS = (
    "non-commercial", "noncommercial", "non_commercial",
    "cc-by-nc", "nc-sa", "nc-nd",
)

CSV_FIELDS = [
    "name", "provider", "category", "hf_id",
    "license", "license_url", "commercial_use",
    "downloads", "likes", "pipeline_tag", "last_modified", "status",
]


def load_tracked():
    with TRACK_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("models", [])


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


def fetch_one(model):
    repo_id = model["hf_id"]
    row = {k: "" for k in CSV_FIELDS}
    row["name"] = model.get("name", repo_id)
    row["provider"] = model.get("provider", "")
    row["category"] = model.get("category", "")
    row["hf_id"] = repo_id
    row["status"] = "pending"

    info = hf_request(repo_id)
    if info is None:
        row["status"] = "not_found"
        return row

    card = info.get("cardData") or {}
    lic, link = parse_license(card)
    row["license"] = lic
    row["license_url"] = link
    row["commercial_use"] = assess_commercial(lic)
    row["downloads"] = info.get("downloads", "")
    row["likes"] = info.get("likes", "")
    row["pipeline_tag"] = info.get("pipeline_tag") or ""
    row["last_modified"] = info.get("lastModified") or ""
    row["status"] = "ok"
    return row


def main():
    if not TRACK_FILE.exists():
        print("Track file not found: {}".format(TRACK_FILE), file=sys.stderr)
        return 1
    models = load_tracked()
    print("Tracking {} models from {}".format(len(models), TRACK_FILE.name))
    rows = []
    for i, m in enumerate(models, 1):
        print("[{}/{}] {}".format(i, len(models), m["hf_id"]))
        rows.append(fetch_one(m))
        if i < len(models):
            time.sleep(REQUEST_DELAY)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(rows),
        "models": rows,
    }
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    ok = sum(1 for r in rows if r["status"] == "ok")
    nf = sum(1 for r in rows if r["status"] == "not_found")
    print("Done. ok={} not_found={}".format(ok, nf))
    return 0


if __name__ == "__main__":
    sys.exit(main())
