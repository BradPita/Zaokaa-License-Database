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

LICENSE_LEGEND = {
    "license_source": {
        "spdx": "标准 SPDX 许可（如 apache-2.0/mit）；license_url 自动指向 spdx.org 官方协议页。",
        "cardata": "许可取自 HuggingFace 仓库 cardData.license 声明；仓库未另附协议链接。",
        "cardata+link": "cardData 声明的许可 + 经 data/license_overrides.json 附加的权威协议原文链接。",
        "cardata+spdx": "cardData 声明的标准 SPDX 许可 + 自动补的 spdx.org 链接。",
        "fallback:<repo>": "cardData 未声明许可；许可由上游仓库 <repo> 推断补齐。",
        "fallback:<repo>+link": "由上游 <repo> 推断补齐 + 附加的权威协议原文链接。",
        "fallback:<repo>+spdx": "由上游 <repo> 推断补齐 + 自动补的 spdx.org 链接。",
    },
    "commercial_use": {
        "Yes": "可商用（宽松开源协议，如 Apache-2.0 / MIT）。",
        "No": "非商用：免费许可不含商用权利，商用须另购许可（如 Krea-2 社区许可、FAIPL）。",
        "Conditional": "有条件商用：满足条款条件（如营收门槛）即可商用，超过门槛须购买商业许可（如 Krea-2 <US$1M、LTX-2 <US$10M 年营收）。",
        "Review": "待人工复核：许可为 other/自定义或未明确，商用属性需人工确认。",
    },
    "commercial_terms": (
        "commercial_use 的审计补充说明：明示商用条件（如营收门槛、须购买商业许可等）。"
        "优先取 data/license_overrides.json 中 fallback/link 的手工 commercial_terms 字段，"
        "否则按 commercial_use 自动生成默认说明。"
    ),
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
    "commercial_use", "commercial_terms", "downloads", "likes", "pipeline_tag",
    "last_modified", "status",
]

# Auto-generated commercial-conditions text used when no manual override
# (fallback/link "commercial_terms") exists for a repo.
DEFAULT_TERMS = {
    "Yes": "Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions.",
    "No": "Non-commercial license: free use excludes commercial rights; commercial use requires a purchased license.",
    "Conditional": "Conditional-commercial license: commercial use permitted when stated conditions are met (e.g. revenue threshold); above the threshold a purchased/commercial license is required.",
    "Review": "Custom or undeclared license; commercial conditions require human review of the license text.",
}


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
        return "", "", ""
    lic = card_data.get("license")
    if isinstance(lic, list):
        lic = ", ".join(str(x) for x in lic if x)
    elif lic is not None:
        lic = str(lic)
    else:
        lic = ""
    lic_name = card_data.get("license_name") or ""
    link = card_data.get("license_link") or ""
    return lic.strip(), (link or "").strip(), (lic_name or "").strip()


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
    lic, link_url, lic_name = parse_license(card)
    if link_url and not link_url.startswith(("http://", "https://")):
        # cardData license_link may be a repo-relative path (e.g. "LICENSE.md")
        link_url = "https://huggingface.co/{}/resolve/main/{}".format(repo, link_url.lstrip("/"))
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
        # license_name (e.g. "circlestone-labs-non-commercial-license") can carry
        # the commercial restriction when cardData.license is just "other".
        commercial = assess_commercial(lic + " " + lic_name)

    if repo in links:
        link_url = links[repo].get("license_url", "")
        source = source + "+link" if source != "cardata" else "cardata+link"
        if links[repo].get("commercial_use"):
            commercial = links[repo]["commercial_use"]

    if not link_url and lic:
        spdx = SPDX_URLS.get(lic.lower().split(",")[0].strip())
        if spdx:
            link_url = spdx
            source = "spdx" if source == "cardata" else source + "+spdx"

    final_commercial = commercial or assess_commercial(lic)
    terms = ""
    if repo in links and links[repo].get("commercial_terms"):
        terms = links[repo]["commercial_terms"]
    elif repo in fallbacks and fallbacks[repo].get("commercial_terms"):
        terms = fallbacks[repo]["commercial_terms"]
    if not terms:
        terms = DEFAULT_TERMS.get(final_commercial, DEFAULT_TERMS["Review"])

    row["license"] = lic
    row["license_url"] = link_url
    row["license_source"] = source
    row["commercial_use"] = final_commercial
    row["commercial_terms"] = terms
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

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_count": len(rows),
        "_sources": ["HuggingFace API (cardData)", "data/models_manifest.json", "data/license_overrides.json (manual fallbacks+links)"],
        "_usage": (
            "HuggingFace 模型仓库许可对照（仓库级）。license 取自 HF cardData 或 fallback（空声明时依上游补齐）；"
            "license_url 为协议原文链接（来源记于 license_source，含义见 _license_legend）；"
            "commercial_use 含义见 _license_legend（Yes 可商用 / No 非商用须另购 / Review 待复核）；"
            "commercial_terms 为该标记的审计补充说明（有条件商用的营收门槛等），含义见 _license_legend。"
            "数据来源：HF API + data/license_overrides.json 人工校正。本文件可直接作为对外交换资料。"
        ),
        "_license_legend": LICENSE_LEGEND,
        "models": rows,
    }

    # 防空提交：忽略 generated_at 与易变的 HF 统计（downloads/likes/last_modified）做内容比对，
    # 只有许可相关数据真正变化时才重写 JSON/CSV，避免每小时 CI 产生纯 churn 提交。
    def norm(s):
        n = {k: v for k, v in s.items() if k != "generated_at"}
        n["models"] = [
            {k: v for k, v in r.items() if k not in ("downloads", "likes", "last_modified")}
            for r in s.get("models", [])
        ]
        return n

    changed = True
    if OUT_JSON.exists():
        try:
            old = json.loads(OUT_JSON.read_text(encoding="utf-8"))
            changed = norm(snapshot) != norm(old)
        except Exception:
            changed = True
    if changed:
        OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            w.writeheader()
            w.writerows(rows)
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
