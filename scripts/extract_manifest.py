#!/usr/bin/env python3
"""
Extract a model manifest from a model_checker.py-style file.

A model manifest stores each model as a CSV-like string literal:
    'category,filename,size,flag,modelscope_url,huggingface_url'
This script extracts them into data/models_manifest.json, keeping only the
Hugging Face source (the ModelScope mirror URL is dropped).

Optional scrubbing: pass --scrub PATH to a file (JSON list or one term per line)
of substrings; entries whose repo or filename contains any term are dropped.
This lets you keep internal distribution-brand references out of a public fork
without baking any specific terms into the code.

Usage:
    python scripts/extract_manifest.py --checker /path/to/model_checker.py [--scrub /path/to/scrub_terms]
    # or:  MODEL_CHECKER=/path/to/model_checker.py python scripts/extract_manifest.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "models_manifest.json"
DEFAULT_CHECKER = ROOT / "data" / "model_checker.py"

ENTRY_RE = re.compile(
    r"""(['"])([^'"\n]*?,[^'"\n]*?,\d+,\d+,https?://[^'"\n]*?,https?://[^'"\n]*?)\1"""
)


def load_scrub_terms(path):
    if not path:
        return []
    text = Path(path).read_text(encoding="utf-8")
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return [str(t).lower() for t in data if t]
    except json.JSONDecodeError:
        pass
    return [ln.strip().lower() for ln in text.splitlines() if ln.strip()]


def repo_from_url(url):
    u = urlparse(url.strip())
    if "huggingface.co" not in u.netloc.lower():
        return ""
    seg = [s for s in u.path.split("/") if s]
    if len(seg) >= 2 and seg[0] not in ("resolve", "tree", "blob"):
        return seg[0] + "/" + seg[1]
    return ""


def extract(text, scrub_terms):
    files = []
    seen = set()
    dropped = 0
    for _, body in ENTRY_RE.findall(text):
        parts = body.split(",")
        if len(parts) < 6:
            continue
        cat = parts[0].strip()
        fname = parts[1].strip()
        hf = parts[-1].strip()
        repo = repo_from_url(hf)
        if not repo:
            continue
        if scrub_terms:
            blob = (repo + " " + fname).lower()
            if any(t in blob for t in scrub_terms):
                dropped += 1
                continue
        key = (cat, fname)
        if key in seen:
            continue
        seen.add(key)
        files.append({"category": cat, "filename": fname, "hf_repo": repo, "hf_url": hf})
    return files, dropped


def main():
    ap = argparse.ArgumentParser(description="Extract a model manifest from model_checker.py")
    ap.add_argument("--checker", default=os.environ.get("MODEL_CHECKER", str(DEFAULT_CHECKER)))
    ap.add_argument("--scrub", default=None, help="optional file of substrings to drop")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    p = Path(args.checker)
    if not p.exists():
        print("model manifest not found: {}".format(p), file=sys.stderr)
        return 1
    scrub_terms = load_scrub_terms(args.scrub) if args.scrub else []
    files, dropped = extract(p.read_text(encoding="utf-8", errors="replace"), scrub_terms)
    out = {
        "_source": "model manifest (model_checker.py style)",
        "_extracted_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "repo_count": len({f["hf_repo"] for f in files}),
        "scrubbed_entries": dropped,
        "files": files,
    }
    op = Path(args.out)
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Extracted {} files / {} repos (scrubbed {} entries) -> {}".format(
        out["file_count"], out["repo_count"], dropped, op))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
