# Zaokaa License Database

An auto-updated lookup table of **open-source / open-weight model licenses** for the models used by a ComfyUI-based generation pipeline - what license each model ships under, plus a best-effort commercial-use flag and **derivative-to-base-model tracing**.

The model inventory is extracted from the pipeline's own model manifest (`model_checker.py`), so it tracks the **real** models in production - Wan2.2, FLUX.2, Krea-2, Qwen-Image, Qwen3-TTS, LTX-2.3, Z-Image, Bernini-R, SCAIL-2, and more. Distribution-brand references are scrubbed from the public data.

The `data/model_license_map.json` artifact feeds a downstream compliance tool: it maps each local model file to its license (for filling the license column of a generation compliance log from the `Base Model` filename).

## How it works

1. `scripts/extract_manifest.py` - reads a `model_checker.py`-style manifest and writes `data/models_manifest.json` (local filename -> Hugging Face repo; distribution-brand entries scrubbed). Re-run when the pipeline's model set changes.
2. `scripts/fetch_licenses.py` - queries the [Hugging Face Hub REST API](https://huggingface.co/docs/huggingface_hub) for each unique repo's `cardData.license` -> `data/licenses_output.csv` + `.json` (one row per repo, including base models).
3. `scripts/build_lookup.py` - joins the manifest + licenses + `data/base_models.json` -> `data/model_license_map.json` (filename -> license, with derivative tracing).
4. `scripts/generate_readme.py` - renders the table below.
5. `.github/workflows/update_licenses.yml` - re-runs steps 2–4 weekly and auto-commits results.

No web scraping, no API key required for public metadata. Pure stdlib Python.

## Derivative model policy

Files whose name contains a **derivative marker** - `nsfw`, `abliterated`, `remix`, `rapid`, `aio`, `merge`, `finetune` - are **downgraded to `Review`**, because a community merge/finetune may mix in non-commercial components even when the base is permissive.

Each derivative is **traced up to its original base model** (registry in `data/base_models.json`), so the association is queryable. The **base model is marked according to its own declaration** on its original HF repo. So a derivative entry carries both its (downgraded) review status and the base model's original license.

## License table

<!-- LICENSE_TABLE_START -->
_Last updated: 2026-08-01 03:32 UTC · 0 tracked repos + 0 base models_

> _No data yet. Run `python scripts/fetch_licenses.py` then `python scripts/generate_readme.py` (or trigger the GitHub Actions workflow) to populate this table._
<!-- LICENSE_TABLE_END -->

## Refresh the model inventory

```bash
python scripts/extract_manifest.py --checker /path/to/model_checker.py
```

The snapshot `data/models_manifest.json` is committed; CI then re-fetches licenses for any new repos. Add ad-hoc reference models (not in the manifest) via `data/extra_models.json` (same `{"files": [...]}` shape). Extend base-model tracing via `data/base_models.json`.

## Run the pipeline locally

```bash
python scripts/fetch_licenses.py        # repo -> license (needs network)
python scripts/build_lookup.py          # filename -> license map (with base tracing)
python scripts/generate_readme.py       # render README table
```

Set `HF_TOKEN` for a higher rate limit / gated-model metadata (optional).

## Trigger a manual update

GitHub -> **Actions** -> *Update Model Licenses* -> **Run workflow**. Also runs every Monday 00:00 UTC.

## Downstream compliance integration

`data/model_license_map.json` is keyed by local filename. Look up a generation's `Base Model` value (e.g. `wan2.1_14B_SCAIL_2_fp8_scaled.safetensors`) to get its `license`. For derivative files, `derivative=true` and the `base_model` / `base_license` fields show the upstream association.

## ⚠️ Disclaimer

The **Commercial** column and the lookup map are **automated heuristics, not legal advice**:

- `Yes` - repo declares a well-known permissive SPDX id (e.g. `apache-2.0`, `mit`).
- `No` - license text contains a non-commercial restriction.
- `Review` - anything else (custom, RAIL, community, repackaged, or derivative). **Always read the actual license** before commercial use.

Repackaged / community re-upload repos may not redeclare the original model's license; the original author's terms still apply. License terms can change. Always verify against the upstream model card. No warranty, no liability.

## License

The scripts and tooling in this repository are released under the **MIT License**. The model license metadata recorded here belongs to the respective model authors.
