#!/usr/bin/env python3
"""
Extract the SimpAI / ComfyUI model manifest from a model_checker.py file.

model_checker.py stores each model as a CSV-like string literal:
    'category,filename,size,flag,modelscope_url,huggingface_url'
This script extracts them into data/simpai_models.json so the license
fetcher and the pmplus bridge can consume them.

Usage:
    python scripts/extract_simpai_models.py --checker /path/to/model_checker.py
    # or:  SIMPAI_MODEL_CHECKER=/path/to/model_checker.py python scripts/extract_simpai_models.py
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
OUT = ROOT / "data" / "simpai_models.json"
DEFAULT_CHECKER = ROOT / "data" / "model_checker.py"

ENTRY_RE = re.compile(
    r"""(['"])([^'"\n]*?,[^'"\n]*?,\d+,\d+,https?://[^'"\n]*?,https?://[^'"\n]*?)\1"""
)


def repo_from_url(url):
    u = urlparse(url.strip())
    if "huggingface.co" not in u.netloc.lower():
        return ""
    seg = [s for s in u.path.split("/") if s]
    if len(seg) >= 2 and seg[0] not in ("resolve", "tree", "blob"):
        return seg[0] + "/" + seg[1]
    return ""


def extract(text):
    files = []
    seen = set()
    for _, body in ENTRY_RE.findall(text):
        parts = body.split(",")
        if len(parts) < 6:
            continue
        cat = parts[0].strip()
        fname = parts[1].strip()
        ms = parts[-2].strip()
        hf = parts[-1].strip()
        repo = repo_from_url(hf)
        key = (cat, fname)
        if key in seen:
            continue
        seen.add(key)
        files.append({
            "category": cat,
            "filename": fname,
            "hf_repo": repo,
            "hf_url": hf,
            "ms_url": ms,
        })
    return files


def main():
    ap = argparse.ArgumentParser(description="Extract SimpAI model manifest from model_checker.py")
    ap.add_argument("--checker", default=os.environ.get("SIMPAI_MODEL_CHECKER", str(DEFAULT_CHECKER)))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    p = Path(args.checker)
    if not p.exists():
        print("model_checker.py not found: {}".format(p), file=sys.stderr)
        return 1
    files = extract(p.read_text(encoding="utf-8", errors="replace"))
    out = {
        "_source": "SimpAI_Studio/model_checker.py",
        "_extracted_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "repo_count": len({f["hf_repo"] for f in files if f["hf_repo"]}),
        "files": files,
    }
    op = Path(args.out)
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Extracted {} files / {} repos -> {}".format(out["file_count"], out["repo_count"], op))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
