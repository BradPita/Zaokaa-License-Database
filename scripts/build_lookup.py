#!/usr/bin/env python3
"""
Build the filename -> license lookup consumed by downstream compliance tooling
(and shareable with clients).

Joins:
  data/models_manifest.json   (filename -> hf_repo)
  data/licenses_output.json   (hf_repo -> license, license_url, license_source)
  data/base_models.json       (original model registry)
into:
  data/model_license_map.json (filename -> license, license_url, license_source,
  with base-model tracing for derivatives).

Derivative policy (per spec):
  Files whose name contains a derivative marker
  (nsfw / abliterated / remix / rapid / aio / merge / finetune) are DOWNGRADED
  to "Review", but each is traced UP to its original base model so the
  association is queryable. The base model itself is marked according to its
  OWN declaration on its original HF repo; base_license_url links to that
  declaration / authoritative license text.

Stdlib only.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "models_manifest.json"
LIC = ROOT / "data" / "licenses_output.json"
BASE = ROOT / "data" / "base_models.json"
OUT = ROOT / "data" / "model_license_map.json"

DERIVATIVE_MARKERS = (
    "nsfw", "abliterated", "remix", "rapid", "aio", "merge", "finetune",
)


def load_bases():
    if not BASE.exists():
        return []
    return json.loads(BASE.read_text(encoding="utf-8")).get("bases", [])


def base_match(bases, filename, repo):
    blob = (filename + " " + repo).lower()
    for b in bases:
        for kw in b.get("keywords", []):
            if kw in blob:
                return b
    return None


def repo_license_url(repo_lic):
    return (repo_lic.get("license_url") or "").strip()


def repo_license_source(repo_lic):
    return (repo_lic.get("license_source") or "").strip()


def resolve_derivative(filename, repo, repo_lic, bases, lic_by_repo):
    out = {
        "derivative": True,
        "license": "待确认（衍生/合并模型）",
        "license_url": repo_license_url(repo_lic),
        "license_source": repo_license_source(repo_lic),
        "commercial": "Review",
        "base_model": "",
        "base_repo": "",
        "base_license": "",
        "base_license_url": "",
        "base_commercial": "",
    }
    base = base_match(bases, filename, repo)
    if not base:
        out.update({"base_model": "未识别", "base_license": "待确认", "base_commercial": "Review"})
        return out
    base_repo = base.get("hf_repo", "")
    be = lic_by_repo.get(base_repo, {})
    base_license = (be.get("license") or "").strip()
    base_status = (be.get("status") or "").strip()
    if not base_repo:
        bl = "待确认（无基础仓库）"
    elif base_status == "not_found":
        bl = "待确认（基础仓库未找到）"
    elif not base_license:
        bl = "待确认（基础模型未声明许可）"
    else:
        bl = base_license
    out.update({
        "base_model": base.get("display", ""),
        "base_repo": base_repo,
        "base_license": bl,
        "base_license_url": repo_license_url(be),
        "base_commercial": (be.get("commercial_use") or "").strip() or "Review",
    })
    return out


def resolve_plain(repo, repo_lic):
    out = {
        "derivative": False,
        "license": "",
        "license_url": repo_license_url(repo_lic),
        "license_source": repo_license_source(repo_lic),
        "commercial": "",
        "base_model": "",
        "base_repo": "",
        "base_license": "",
        "base_license_url": "",
        "base_commercial": "",
    }
    if not repo:
        out["license"] = "待确认（无HF来源）"
        out["commercial"] = "Review"
        return out
    status = (repo_lic.get("status") or "").strip()
    license_ = (repo_lic.get("license") or "").strip()
    if status == "not_found":
        out["license"] = "待确认（HF仓库未找到）"
        out["commercial"] = "Review"
    elif not license_:
        out["license"] = "待确认（HF未声明许可）"
        out["commercial"] = "Review"
    else:
        out["license"] = license_
        out["commercial"] = (repo_lic.get("commercial_use") or "").strip() or "Review"
    return out


def main():
    if not MANIFEST.exists():
        print("models_manifest.json not found. Run extract_manifest.py first.", file=sys.stderr)
        return 1
    if not LIC.exists():
        print("licenses_output.json not found. Run fetch_licenses.py first.", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lic = json.loads(LIC.read_text(encoding="utf-8"))
    lic_by_repo = {m["hf_id"]: m for m in lic.get("models", [])}
    bases = load_bases()

    entries = []
    deriv_count = 0
    for f in manifest.get("files", []):
        filename = f.get("filename", "")
        repo = f.get("hf_repo", "")
        repo_lic = lic_by_repo.get(repo, {})
        tokens = set(re.split(r"[-_./\s]+", filename.lower()))
        is_deriv = any(mk in tokens for mk in DERIVATIVE_MARKERS)
        if is_deriv:
            res = resolve_derivative(filename, repo, repo_lic, bases, lic_by_repo)
            deriv_count += 1
        else:
            res = resolve_plain(repo, repo_lic)
        entries.append({
            "category": f.get("category", ""),
            "filename": filename,
            "hf_repo": repo,
            "derivative": res["derivative"],
            "license": res["license"],
            "license_url": res["license_url"],
            "license_source": res["license_source"],
            "commercial": res["commercial"],
            "base_model": res["base_model"],
            "base_repo": res["base_repo"],
            "base_license": res["base_license"],
            "base_license_url": res["base_license_url"],
            "base_commercial": res["base_commercial"],
        })

    with_link = sum(1 for e in entries if e["license_url"])
    out = {
        "_generated_at": datetime.now(timezone.utc).isoformat(),
        "_sources": ["models_manifest.json", "licenses_output.json", "base_models.json"],
        "_usage": (
            "filename 为键查询。license 为建议填入值，license_url 为协议原文链接（carddata/fallback/link 来源记于 license_source）；"
            "commercial 为 Review/待确认 时需人工复核。derivative=true 的条目已向上溯源至 base_model，"
            "base_license 依据基础模型原声明，base_license_url 为其协议链接。本文件可直接作为对外交换资料。"
        ),
        "_license_legend": lic.get("_license_legend"),
        "derivative_markers": list(DERIVATIVE_MARKERS),
        "file_count": len(entries),
        "derivative_count": deriv_count,
        "files_with_license_url": with_link,
        "files": entries,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote {} entries ({} derivative, {} with license_url) -> {}".format(
        len(entries), deriv_count, with_link, OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
