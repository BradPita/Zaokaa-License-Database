# Zaokaa License Database

An auto-updated lookup table of **open-source / open-weight model licenses** for the models actually used by the **SimpAI Studio** (ComfyUI) pipeline - what license each model ships under and a best-effort commercial-use flag.

The model inventory is sourced from SimpAI's own `model_checker.py` (the authoritative manifest of every checkpoint/LoRA/encoder SimpAI and the ComfyUI API use), so this tracks the **real** models in production - Wan2.2, FLUX.2, Krea-2, Qwen-Image, Qwen3-TTS, LTX-2.3, Z-Image, Bernini-R, SCAIL-2, and more.

Built to feed the **pmplus** AIGC-compliance toolchain's model-license data (the `许可` column of its compliance CSV, derived from each generation's `Base Model` filename).

## How it works

1. `scripts/extract_simpai_models.py` - reads `model_checker.py` and writes `data/simpai_models.json` (local filename → Hugging Face repo). Run this when SimpAI updates its model set.
2. `scripts/fetch_licenses.py` - queries the [Hugging Face Hub REST API](https://huggingface.co/docs/huggingface_hub) for each unique repo's `cardData.license` → `data/licenses_output.csv` + `.json` (one row per repo).
3. `scripts/build_pmplus_map.py` - joins the file manifest with the licenses → `data/pmplus_license_map.json` (local filename → suggested license, for pmplus).
4. `scripts/generate_readme.py` - renders the table below.
5. `.github/workflows/update_licenses.yml` - re-runs steps 2–4 weekly and auto-commits results.

No web scraping, no API key required for public metadata. Pure stdlib Python.

## License table

<!-- LICENSE_TABLE_START -->
_Last updated: 2026-08-01 02:56 UTC · 0 repos tracked_

> _No data yet. Run `python scripts/fetch_licenses.py` then `python scripts/generate_readme.py` (or trigger the GitHub Actions workflow) to populate this table._
<!-- LICENSE_TABLE_END -->

## Refresh the model inventory

When SimpAI's `model_checker.py` changes (new models added):

```bash
python scripts/extract_simpai_models.py --checker /path/to/SimpAI_Studio/model_checker.py
```

The snapshot `data/simpai_models.json` is committed to this repo; CI then re-fetches licenses for any new repos. Add ad-hoc reference models (not in SimpAI) by creating `data/extra_models.json` with the same `{"files": [...]}` shape.

## Run the pipeline locally

```bash
python scripts/fetch_licenses.py        # repo -> license (needs network)
python scripts/build_pmplus_map.py      # filename -> license map
python scripts/generate_readme.py       # render README table
```

Set `HF_TOKEN` for a higher rate limit / gated-model metadata (optional).

## Trigger a manual update

GitHub → **Actions** → *Update Model Licenses* → **Run workflow**. Also runs every Monday 00:00 UTC.

## pmplus integration

`data/pmplus_license_map.json` is keyed by local filename. In pmplus's `log.html` parser, look up the `Base Model` value (e.g. `wan2.1_14B_SCAIL_2_fp8_scaled.safetensors`) to fill the compliance CSV `许可` column. Files whose names look like custom merges/finetunes are conservatively flagged for human review even when the base repo is permissive.

## ⚠️ Disclaimer

The **Commercial** column and the pmplus map are **automated heuristics, not legal advice**:

- `Yes` - repo declares a well-known permissive SPDX id (e.g. `apache-2.0`, `mit`).
- `No` - license text contains a non-commercial restriction.
- `Review` - anything else (custom, RAIL, community, repackaged, or merged). **Always read the actual license** before commercial use.

Repackaged / community re-upload repos (e.g. `Comfy-Org/*`, `silveroxides/*`) may not redeclare the original model's license; the original author's terms still apply. License terms can change. Always verify against the upstream model card. No warranty, no liability.
