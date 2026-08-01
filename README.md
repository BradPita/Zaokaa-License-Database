# Zaokaa License Database

A community-maintained, auto-updated lookup table of **open-source / open-weight model licenses** — what license each model ships under (Wan, FLUX, Stable Diffusion, Llama, Qwen, …) and a best-effort commercial-use flag.

Built to complement the **pmplus** project's model usage-license data, and useful for anyone doing commercial AI deployment who is tired of hunting down license terms model-by-model.

## How it works

1. `data/models_to_track.json` — the curated list of models to track (you edit this).
2. `scripts/fetch_licenses.py` — queries the [Hugging Face Hub REST API](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api) for each model's `cardData.license` and writes `data/licenses_output.csv` + `.json`.
3. `scripts/generate_readme.py` — renders the CSV into the table below.
4. `.github/workflows/update_licenses.yml` — re-runs the pipeline weekly (and on manual trigger) and auto-commits the results.

No web scraping, no API keys required for public model metadata. Pure stdlib Python.

## License table

<!-- LICENSE_TABLE_START -->
_Last updated: 2026-08-01 02:33 UTC · 0 models tracked_

> _No data yet. Run `python scripts/fetch_licenses.py` then `python scripts/generate_readme.py` to populate this table (or trigger the GitHub Actions workflow)._
<!-- LICENSE_TABLE_END -->

## Add a model

Append an entry to `data/models_to_track.json`:

```json
{ "name": "My Model", "provider": "Org", "category": "image", "hf_id": "org/repo-name" }
```

Valid `category` values: `image`, `video`, `llm`, `audio` (others work too — they get their own section). `hf_id` is the Hugging Face Hub repo path (`org/name`).

## Run locally

```bash
python scripts/fetch_licenses.py      # populate data/licenses_output.csv
python scripts/generate_readme.py    # render into README.md
```

Set `HF_TOKEN` in your environment for a higher rate limit / gated-model metadata (optional).

## Trigger a manual update

GitHub → **Actions** → *Update Model Licenses* → **Run workflow**. The workflow also runs automatically every Monday at 00:00 UTC.

## ⚠️ Disclaimer

The **Commercial** column is an **automated heuristic, not legal advice**:

- `Yes` — license is a well-known permissive SPDX id (e.g. `apache-2.0`, `mit`).
- `No` — license text contains a non-commercial restriction.
- `Review` — anything else (custom, RAIL, community, or gated-license terms). **Always read the actual license** before commercial use.

License terms can change. Always verify against the upstream model card. This project provides no warranty and accepts no liability for licensing decisions made using this data.

## License

The scripts and tooling in this repository are released under the **MIT License**. The model license metadata recorded here belongs to the respective model authors.
