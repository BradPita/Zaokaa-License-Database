#!/usr/bin/env python3
"""
Build the pmplus-consumable license lookup: local filename -> license.

Joins:
  data/simpai_models.json   (filename -> hf_repo)
  data/licenses_output.json (hf_repo -> license)
into:
  data/pmplus_license_map.json (filename -> suggested 许可 value)

This is what pmplus's compliance CSV filler consumes to populate the 许可
column from the Base Model (local safetensors filename) field in log.html.

Conservative policy: any file whose name looks like a custom merge / finetune
(see MERGE_MARKERS) is flagged for human review even if the base repo is
permissive, because a merge can mix in non-commercial components.

Stdlib only.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIMPAI = ROOT / "data" / "simpai_models.json"
LIC = ROOT / "data" / "licenses_output.json"
OUT = ROOT / "data" / "pmplus_license_map.json"

MERGE_MARKERS = (
    # Tokens that strongly indicate a community-derived merge / finetune that
    # may mix in non-commercial components. Official accelerated variants
    # (SCAIL / Lightning / Turbo / Edit / Lite) inherit the base repo license
    # and are NOT flagged here.
    "nsfw", "abliterated", "uncensored", "uncens", "remix", "rapid",
    "aio", "merge", "finetune", "fine-tune",
)


def resolve(f, repo_lic):
    repo = f.get("hf_repo", "")
    fname = f.get("filename", "")
    info = repo_lic.get(repo, {})
    license_ = (info.get("license") or "").strip()
    commercial = (info.get("commercial_use") or "").strip()
    status = (info.get("status") or "").strip()

    if not repo:
        return "待确认（无HF来源）", "Review", ""
    if status == "not_found":
        return "待确认（HF仓库未找到）", "Review", ""
    low = fname.lower()
    is_merge = any(mk in low for mk in MERGE_MARKERS)
    if is_merge and commercial == "Yes":
        return license_ + "（含微调/合并，需人工确认）", "Review", license_
    if license_:
        return license_, commercial, license_
    return "待确认（HF未声明许可）", "Review", ""


def main():
    if not SIMPAI.exists():
        print("simpai_models.json not found. Run extract_simpai_models.py first.", file=sys.stderr)
        return 1
    if not LIC.exists():
        print("licenses_output.json not found. Run fetch_licenses.py first.", file=sys.stderr)
        return 1

    simpai = json.loads(SIMPAI.read_text(encoding="utf-8"))
    lic = json.loads(LIC.read_text(encoding="utf-8"))
    repo_lic = {m["hf_id"]: m for m in lic.get("models", [])}

    entries = []
    for f in simpai.get("files", []):
        lic_val, comm, base = resolve(f, repo_lic)
        entries.append({
            "category": f.get("category", ""),
            "filename": f.get("filename", ""),
            "hf_repo": f.get("hf_repo", ""),
            "license": lic_val,
            "commercial": comm,
            "base_license": base,
        })

    out = {
        "_generated_at": datetime.now(timezone.utc).isoformat(),
        "_sources": ["simpai_models.json", "licenses_output.json"],
        "_usage": (
            "pmplus 合规CSV「许可」列填充：以本地模型文件名(filename)为键查询本表。"
            "license 字段为建议填入值；commercial 为 Review/待确认 时需人工复核。"
            "含微调/合并特征词的文件即使基础仓库宽松也降级为需复核。"
        ),
        "merge_markers": list(MERGE_MARKERS),
        "file_count": len(entries),
        "files": entries,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote {} entries -> {}".format(len(entries), OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
