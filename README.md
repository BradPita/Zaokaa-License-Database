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
_Last updated: 2026-08-01 08:15 UTC · 59 tracked repos + 7 base models_

## Tracked models

### Wan

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/Wan_2.1_ComfyUI_repackaged](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged) | Comfy-Org | [apache-2.0](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B) | Yes | 3 | 2,198,113 | 2026-01-28 |
| [Comfy-Org/Wan_2.2_ComfyUI_Repackaged](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged) | Comfy-Org | [apache-2.0](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B) | Yes | 1 | 5,284,364 | 2026-07-03 |
| [FX-FeiHou/wan2.2-Remix](https://huggingface.co/FX-FeiHou/wan2.2-Remix) | FX-FeiHou | other | Review | 1 | 2 | 2026-03-24 |
| [Kijai/WanVideo_comfy](https://huggingface.co/Kijai/WanVideo_comfy) | Kijai | [apache-2.0](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B) | Yes | 5 | 1,834,935 | 2026-06-13 |
| [Wan-AI/Wan2.2-Animate-14B](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B) | Wan-AI | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 20,293 | 2025-11-05 |
| [rzgar/NSFW-Wan-UMT5-XXL-V2](https://huggingface.co/rzgar/NSFW-Wan-UMT5-XXL-V2) | rzgar | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 164 | 2026-07-17 |
| [rzgar/Wan2.2_I2V_LightX2V_2Step](https://huggingface.co/rzgar/Wan2.2_I2V_LightX2V_2Step) | rzgar | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 1,314 | 2026-07-17 |
| [spacepxl/Wan2.1-VAE-upscale2x](https://huggingface.co/spacepxl/Wan2.1-VAE-upscale2x) | spacepxl | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 49,026 | 2025-10-26 |

### FLUX

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [silveroxides/FLUX.2-dev-fp8_scaled](https://huggingface.co/silveroxides/FLUX.2-dev-fp8_scaled) | silveroxides | [other](https://huggingface.co/black-forest-labs/FLUX.2-dev/blob/main/LICENSE.md) | Review | 1 | 16,114 | 2026-07-15 |

### Krea

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/Krea-2](https://huggingface.co/Comfy-Org/Krea-2) | Comfy-Org | [other](https://github.com/krea-ai/krea-2/blob/main/LICENSE.md) | Review | 3 | 10 | 2026-07-20 |
| [conradlocke/krea2-identity-edit](https://huggingface.co/conradlocke/krea2-identity-edit) | conradlocke | [other](https://krea.ai/krea-2-licensing) | Review | 1 | 0 | 2026-07-29 |
| [uzumix/krea2filterbypass3.safetensors](https://huggingface.co/uzumix/krea2filterbypass3.safetensors) | uzumix | [other](https://github.com/krea-ai/krea-2/blob/main/LICENSE.md) | Review | 1 | 4,093 | 2026-07-08 |

### Qwen-Image

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/Qwen-Image-Edit_ComfyUI](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 821,932 | 2026-07-01 |
| [Comfy-Org/Qwen-Image_ComfyUI](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 1,846,848 | 2026-06-06 |
| [Phr00t/Qwen-Image-Edit-Rapid-AIO](https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO) | Phr00t | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 0 | 2026-02-03 |
| [QuantFunc/Nunchaku-Qwen-Image-EDIT-2511](https://huggingface.co/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511) | QuantFunc | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 4,396 | 2026-06-19 |
| [fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA](https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA) | fal | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 63,422 | 2026-01-07 |
| [lightx2v/Qwen-Image-2512-Lightning](https://huggingface.co/lightx2v/Qwen-Image-2512-Lightning) | lightx2v | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 70,227 | 2026-01-15 |
| [lightx2v/Qwen-Image-Edit-2511-Lightning](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning) | lightx2v | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 289,282 | 2026-01-15 |
| [lrzjason/QwenEdit_Consistance_Edit](https://huggingface.co/lrzjason/QwenEdit_Consistance_Edit) | lrzjason | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 0 | 2026-04-17 |

### Qwen-TTS

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Qwen/Qwen3-TTS-12Hz-0.6B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 12 | 424,964 | 2026-01-29 |
| [Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 12 | 1,620,538 | 2026-01-29 |
| [Qwen/Qwen3-TTS-12Hz-1.7B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 12 | 2,482,881 | 2026-01-23 |
| [Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 12 | 2,452,950 | 2026-01-29 |
| [Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 12 | 650,372 | 2026-01-29 |
| [Qwen/Qwen3-TTS-Tokenizer-12Hz](https://huggingface.co/Qwen/Qwen3-TTS-Tokenizer-12Hz) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 4 | 104,505 | 2026-01-29 |

### Qwen3-LLM

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [mradermacher/Huihui-Qwen3.5-9B-abliterated-GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.5-9B-abliterated-GGUF) | mradermacher | [apache-2.0](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE) | Yes | 2 | 15,817 | 2026-03-10 |

### LTX-Video

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/ltx-2](https://huggingface.co/Comfy-Org/ltx-2) | Comfy-Org | [other](https://github.com/Lightricks/LTX-2/blob/main/LICENSE) | Review | 2 | 0 | 2026-03-08 |
| [Kijai/LTX2.3_comfy](https://huggingface.co/Kijai/LTX2.3_comfy) | Kijai | [other](https://github.com/Lightricks/LTX-2/blob/main/LICENSE) | Review | 6 | 999,703 | 2026-07-28 |
| [Lightricks/LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3) | Lightricks | [other](https://github.com/Lightricks/LTX-2/blob/main/LICENSE) | Review | 1 | 2,192,827 | 2026-07-09 |
| [joyfox/LTX2.3-ICEdit-Insight](https://huggingface.co/joyfox/LTX2.3-ICEdit-Insight) | joyfox | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 4 | 63,228 | 2026-07-23 |
| [oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint](https://huggingface.co/oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint) | oumoumad | [other](https://github.com/Lightricks/LTX-2/blob/main/LICENSE) | Review | 1 | 0 | 2026-04-10 |

### Z-Image

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/z_image_turbo](https://huggingface.co/Comfy-Org/z_image_turbo) | Comfy-Org | [apache-2.0](https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1) | Yes | 2 | 5,218,592 | 2026-07-02 |
| [alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1](https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1) | alibaba-pai | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 75,682 | 2026-02-26 |

### Bernini

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/Bernini-R](https://huggingface.co/Comfy-Org/Bernini-R) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 0 | 2026-06-30 |
| [rzgar/Bernini-R-LightX2V-4step-loras](https://huggingface.co/rzgar/Bernini-R-LightX2V-4step-loras) | rzgar | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 18,640 | 2026-07-02 |

### SCAIL

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/SCAIL-2](https://huggingface.co/Comfy-Org/SCAIL-2) | Comfy-Org | [mit](https://spdx.org/licenses/MIT.html) | Yes | 2 | 0 | 2026-07-15 |

### SeedVR

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [numz/SeedVR2_comfyUI](https://huggingface.co/numz/SeedVR2_comfyUI) | numz | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 212,750 | 2025-11-09 |

### Segment Anything

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/sam3.1](https://huggingface.co/Comfy-Org/sam3.1) | Comfy-Org | [other](https://github.com/facebookresearch/sam3/blob/main/LICENSE) | Review | 1 | 0 | 2026-05-06 |
| [jetjodh/sam-3d-body-dinov3](https://huggingface.co/jetjodh/sam-3d-body-dinov3) | jetjodh | [other](https://huggingface.co/facebook/sam-3d-body-dinov3/blob/main/LICENSE) | Review | 3 | 1,206 | 2025-11-25 |

### LivePortrait

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Kijai/LivePortrait_safetensors](https://huggingface.co/Kijai/LivePortrait_safetensors) | Kijai | [mit](https://huggingface.co/spaces/KlingTeam/LivePortrait/blob/main/LICENSE) | Yes | 5 | 0 | 2024-08-02 |

### Pose

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Comfy-Org/SDPose](https://huggingface.co/Comfy-Org/SDPose) | Comfy-Org | [mit](https://spdx.org/licenses/MIT.html) | Yes | 1 | 25,368 | 2026-03-03 |
| [Kijai/vitpose_comfy](https://huggingface.co/Kijai/vitpose_comfy) | Kijai | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 0 | 2025-09-23 |
| [hr16/DWPose-TorchScript-BatchSize5](https://huggingface.co/hr16/DWPose-TorchScript-BatchSize5) | hr16 | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 0 | 2023-11-30 |
| [yzd-v/DWPose](https://huggingface.co/yzd-v/DWPose) | yzd-v | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 0 | 2023-08-22 |

### PoseStudio

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [MIUProject/VNCCS_PoseStudio](https://huggingface.co/MIUProject/VNCCS_PoseStudio) | MIUProject | [mit](https://spdx.org/licenses/MIT.html) | Yes | 1 | 0 | 2026-05-23 |
| [MIUProject/VNCCS_PoseStudio_Klein](https://huggingface.co/MIUProject/VNCCS_PoseStudio_Klein) | MIUProject | [mit](https://spdx.org/licenses/MIT.html) | Yes | 1 | 0 | 2026-07-21 |

### Audio

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Kijai/MelBandRoFormer_comfy](https://huggingface.co/Kijai/MelBandRoFormer_comfy) | Kijai | [mit](https://huggingface.co/KimberleyJSN/melbandroformer/blob/main/README.md) | Yes | 1 | 93,004 | 2025-08-23 |
| [Kijai/wav2vec2_safetensors](https://huggingface.co/Kijai/wav2vec2_safetensors) | Kijai | [mit](https://spdx.org/licenses/MIT.html) | Yes | 3 | 0 | 2025-08-25 |

### Anima

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [circlestone-labs/Anima](https://huggingface.co/circlestone-labs/Anima) | circlestone-labs | [other](LICENSE.md) | Review | 2 | 851,880 | 2026-07-24 |
| [kohya-ss/Anima-LLLite](https://huggingface.co/kohya-ss/Anima-LLLite) | kohya-ss | [other](LICENSE) | Review | 1 | 0 | 2026-05-20 |

### Kaloscope

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [heathcliff01/Kaloscope](https://huggingface.co/heathcliff01/Kaloscope) | heathcliff01 | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2 | 0 | 2025-10-20 |

### Bingsu

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Bingsu/adetailer](https://huggingface.co/Bingsu/adetailer) | Bingsu | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 10,272,979 | 2024-11-21 |

### ChenkinNoob

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [ChenkinNoob/Chenkin-UniControl-XL](https://huggingface.co/ChenkinNoob/Chenkin-UniControl-XL) | ChenkinNoob | [fair-ai-public-license-1.0-sd](https://freedevproject.org/faipl-1.0-sd/) | No | 1 | 806 | 2026-04-10 |
| [ChenkinNoob/ChenkinNoob-XL-V0.5](https://huggingface.co/ChenkinNoob/ChenkinNoob-XL-V0.5) | ChenkinNoob | [other](https://freedevproject.org/faipl-1.0-sd/) | Review | 1 | 36 | 2026-04-10 |

### Kim2091

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [Kim2091/AnimeSharp](https://huggingface.co/Kim2091/AnimeSharp) | Kim2091 | [cc-by-nc-sa-4.0](https://spdx.org/licenses/CC-BY-NC-SA-4.0.html) | No | 1 | 0 | 2024-12-08 |

### apple

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [apple/Sharp](https://huggingface.co/apple/Sharp) | apple | [apple-amlr](https://github.com/apple/ml-sharp/blob/main/LICENSE) | Review | 1 | 3,306 | 2025-12-18 |

### lrzjason

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [lrzjason/Anything2Real_2601](https://huggingface.co/lrzjason/Anything2Real_2601) | lrzjason | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 1 | 117,333 | 2026-01-28 |

### mashb1t

| Model | Provider | License | Commercial | Files | Downloads | Updated |
|---|---|---|---|---|---|---|
| [mashb1t/misc](https://huggingface.co/mashb1t/misc) | mashb1t | - | Review | 3 | 0 | 2024-06-16 |

### Base model declarations (for derivative tracing)

> Original models that derivatives trace up to. Marked per each model's own declaration.

| Base model | Repo | License | Commercial | Updated |
|---|---|---|---|---|
| [Qwen/Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2025-08-18 |
| [Qwen/Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2025-12-23 |
| [Qwen/Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2025-04-06 |
| [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | Qwen | [apache-2.0](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE) | Yes | 2025-07-26 |
| [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | Qwen | [apache-2.0](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE) | Yes | 2026-03-02 |
| [Wan-AI/Wan2.1-T2V-14B](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B) | Wan-AI | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | 2025-03-12 |
| [google/gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it) | google | [gemma](https://ai.google.dev/gemma/terms) | Review | 2025-03-21 |

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
