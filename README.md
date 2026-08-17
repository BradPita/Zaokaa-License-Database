# Zaokaa License Database

An auto-updated lookup table of **open-source / open-weight model licenses** for the models used by a ComfyUI-based generation pipeline - what license each model ships under, plus a best-effort commercial-use flag and **derivative-to-base-model tracing**.

The model inventory is extracted from the pipeline's own model manifest (`model_checker.py`), so it tracks the **real** models in production - Wan2.2, FLUX.2, Krea-2, Qwen-Image, Qwen3-TTS, LTX-2.3, Z-Image, Bernini-R, SCAIL-2, and more. Distribution-brand references are scrubbed from the public data.

The `data/model_license_map.json` artifact feeds a downstream compliance tool: it maps each local model file to its license (for filling the license column of a generation compliance log from the `Base Model` filename).

## How it works

1. `scripts/extract_manifest.py` - reads a `model_checker.py`-style manifest and writes `data/models_manifest.json` (local filename -> Hugging Face repo; distribution-brand entries scrubbed). Re-run when the pipeline's model set changes.
2. `scripts/fetch_licenses.py` - queries the [Hugging Face Hub REST API](https://huggingface.co/docs/huggingface_hub) for each unique repo's `cardData.license` -> `data/licenses_output.csv` + `.json` (one row per repo, including base models).
3. `scripts/build_lookup.py` - joins the manifest + licenses + `data/base_models.json` -> `data/model_license_map.json` (filename -> license, with derivative tracing).
4. `scripts/generate_readme.py` - renders the table below.
5. `.github/workflows/update_licenses.yml` - pulls the latest manifest from the upstream model list, then re-runs steps 2–4 hourly and auto-commits only when data actually changed (no-op runs skip committing).

No web scraping, no API key required for public metadata. Pure stdlib Python.

## Derivative model policy

Files whose name contains a **derivative marker** - `nsfw`, `abliterated`, `remix`, `rapid`, `aio`, `merge`, `finetune` - are **downgraded to `Review`**, because a community merge/finetune may mix in non-commercial components even when the base is permissive.

Each derivative is **traced up to its original base model** (registry in `data/base_models.json`), so the association is queryable. The **base model is marked according to its own declaration** on its original HF repo. So a derivative entry carries both its (downgraded) review status and the base model's original license.

## License table

<!-- LICENSE_TABLE_START -->
_Last updated: 2026-08-17 12:25 UTC | 64 tracked repos + 7 base models_

> **[View the formatted table online](https://bradpita.github.io/Zaokaa-License-Database/)** - fixed column widths for side-by-side comparison and every link opens in a new tab (not possible inside GitHub's README).

## Tracked models

### Wan

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/Wan_2.1_ComfyUI_repackaged](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 3 | 2,503,832 | 2026-08-17 |
| [Comfy-Org/Wan_2.2_ComfyUI_Repackaged](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 4,908,111 | 2026-08-17 |
| [FX-FeiHou/wan2.2-Remix](https://huggingface.co/FX-FeiHou/wan2.2-Remix) | FX-FeiHou | [other](https://spdx.org/licenses/Apache-2.0.html) | Review | Custom or undeclared license; commercial conditions require human review of the license text. | 1 | 8 | 2026-03-24 |
| [Kijai/WanVideo_comfy](https://huggingface.co/Kijai/WanVideo_comfy) | Kijai | [apache-2.0](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 5 | 1,680,445 | 2026-06-13 |
| [QuantStack/Wan2.2-I2V-A14B-GGUF](https://huggingface.co/QuantStack/Wan2.2-I2V-A14B-GGUF) | QuantStack | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 245,766 | 2025-07-29 |
| [Wan-AI/Wan2.2-Animate-14B](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B) | Wan-AI | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 20,957 | 2025-11-05 |
| [rzgar/NSFW-Wan-UMT5-XXL-V2](https://huggingface.co/rzgar/NSFW-Wan-UMT5-XXL-V2) | rzgar | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 52 | 2026-07-17 |
| [rzgar/Wan2.2_I2V_LightX2V_2Step](https://huggingface.co/rzgar/Wan2.2_I2V_LightX2V_2Step) | rzgar | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 1,035 | 2026-07-17 |
| [spacepxl/Wan2.1-VAE-upscale2x](https://huggingface.co/spacepxl/Wan2.1-VAE-upscale2x) | spacepxl | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 35,928 | 2025-10-26 |

### FLUX

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [silveroxides/FLUX.2-dev-fp8_scaled](https://huggingface.co/silveroxides/FLUX.2-dev-fp8_scaled) | silveroxides | [other](https://huggingface.co/black-forest-labs/FLUX.2-dev/blob/main/LICENSE.md) | No | Black Forest Labs FLUX.2 \[dev\] Non-Commercial License: non-commercial, non-production use; commercial use requires a separate license from BFL. | 1 | 14,497 | 2026-07-15 |

### Krea

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/Krea-2](https://huggingface.co/Comfy-Org/Krea-2) | Comfy-Org | [other](https://cdn.jsdelivr.net/gh/krea-ai/krea-2@db3984fbc6e13b34c0064990fc2d95ac64d00058/assets/hf_samples/LICENSE.pdf) | Conditional | Krea 2 Community License v1 (2026-06-22): free commercial use below US$1M company-wide annual revenue; >=US$1M requires a paid Enterprise License (opensource@krea.ai); AUP + content-filter obligations apply. | 3 | 2,092,440 | 2026-08-17 |
| [conradlocke/krea2-identity-edit](https://huggingface.co/conradlocke/krea2-identity-edit) | conradlocke | [other](https://cdn.jsdelivr.net/gh/krea-ai/krea-2@db3984fbc6e13b34c0064990fc2d95ac64d00058/assets/hf_samples/LICENSE.pdf) | Conditional | Krea 2 Community License v1 (2026-06-22): free commercial use below US$1M company-wide annual revenue; >=US$1M requires a paid Enterprise License (opensource@krea.ai); AUP + content-filter obligations apply. | 1 | 0 | 2026-07-29 |
| [uzumix/krea2filterbypass3.safetensors](https://huggingface.co/uzumix/krea2filterbypass3.safetensors) | uzumix | [other](https://cdn.jsdelivr.net/gh/krea-ai/krea-2@db3984fbc6e13b34c0064990fc2d95ac64d00058/assets/hf_samples/LICENSE.pdf) | Conditional | Krea 2 Community License v1 (2026-06-22): free commercial use below US$1M company-wide annual revenue; >=US$1M requires a paid Enterprise License (opensource@krea.ai); AUP + content-filter obligations apply. | 1 | 3,851 | 2026-07-08 |

### Qwen-Image

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/Qwen-Image-Edit_ComfyUI](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 1,130,805 | 2026-08-17 |
| [Comfy-Org/Qwen-Image_ComfyUI](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 1,742,041 | 2026-08-17 |
| [Phr00t/Qwen-Image-Edit-Rapid-AIO](https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO) | Phr00t | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 0 | 2026-02-03 |
| [QuantFunc/Nunchaku-Qwen-Image-EDIT-2511](https://huggingface.co/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511) | QuantFunc | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 3,568 | 2026-06-19 |
| [fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA](https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA) | fal | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 63,497 | 2026-01-07 |
| [lightx2v/Qwen-Image-2512-Lightning](https://huggingface.co/lightx2v/Qwen-Image-2512-Lightning) | lightx2v | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 71,244 | 2026-01-15 |
| [lightx2v/Qwen-Image-Edit-2511-Lightning](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning) | lightx2v | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 321,465 | 2026-01-15 |
| [lrzjason/QwenEdit_Consistance_Edit](https://huggingface.co/lrzjason/QwenEdit_Consistance_Edit) | lrzjason | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 0 | 2026-04-17 |

### Qwen-TTS

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Qwen/Qwen3-TTS-12Hz-0.6B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 12 | 520,457 | 2026-01-29 |
| [Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 12 | 1,452,762 | 2026-01-29 |
| [Qwen/Qwen3-TTS-12Hz-1.7B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 12 | 3,002,292 | 2026-01-23 |
| [Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 12 | 2,255,320 | 2026-01-29 |
| [Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 12 | 407,578 | 2026-01-29 |
| [Qwen/Qwen3-TTS-Tokenizer-12Hz](https://huggingface.co/Qwen/Qwen3-TTS-Tokenizer-12Hz) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 4 | 170,144 | 2026-01-29 |

### Qwen3-LLM

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [mradermacher/Huihui-Qwen3.5-9B-abliterated-GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.5-9B-abliterated-GGUF) | mradermacher | [apache-2.0](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 34,479 | 2026-03-10 |

### LTX-Video

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [joyfox/LTX2.3-ICEdit-Insight](https://huggingface.co/joyfox/LTX2.3-ICEdit-Insight) | joyfox | [apache-2.0](https://github.com/Lightricks/LTX-2/blob/main/LICENSE) | Conditional | LTX-2 Community License (2026-01-05): free commercial use for entities with company-wide annual revenue below US$10M (affiliates aggregated); >=US$10M requires a paid commercial license (https://ltx.io/model/licensing); Attachment A bans commercial training of competing models. | 4 | 63,655 | 2026-07-23 |
| [oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint](https://huggingface.co/oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint) | oumoumad | [other](https://github.com/Lightricks/LTX-2/blob/main/LICENSE) | Conditional | LTX-2 Community License (2026-01-05): free commercial use for entities with company-wide annual revenue below US$10M (affiliates aggregated); >=US$10M requires a paid commercial license (https://ltx.io/model/licensing); Attachment A bans commercial training of competing models. | 1 | 0 | 2026-04-10 |

### Z-Image

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/z_image_turbo](https://huggingface.co/Comfy-Org/z_image_turbo) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 6,049,162 | 2026-08-17 |
| [alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1](https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1) | alibaba-pai | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 99,549 | 2026-02-26 |

### Bernini

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/Bernini-R](https://huggingface.co/Comfy-Org/Bernini-R) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 99,684 | 2026-08-17 |
| [rzgar/Bernini-R-LightX2V-4step-loras](https://huggingface.co/rzgar/Bernini-R-LightX2V-4step-loras) | rzgar | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 10,958 | 2026-07-02 |

### SCAIL

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/SCAIL-2](https://huggingface.co/Comfy-Org/SCAIL-2) | Comfy-Org | [mit](https://spdx.org/licenses/MIT.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 3 | 341,696 | 2026-08-17 |

### SeedVR

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [numz/SeedVR2_comfyUI](https://huggingface.co/numz/SeedVR2_comfyUI) | numz | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 238,204 | 2025-11-09 |

### Segment Anything

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/sam3.1](https://huggingface.co/Comfy-Org/sam3.1) | Comfy-Org | [other](https://github.com/facebookresearch/sam3/blob/main/LICENSE) | Yes | SAM License (Meta, 2025-11-19): royalty-free commercial use permitted, no revenue threshold; obligations: no reverse engineering of components, trade-control/ITAR compliance, acknowledge SAM in publications. | 1 | 142,561 | 2026-08-17 |
| [jetjodh/sam-3d-body-dinov3](https://huggingface.co/jetjodh/sam-3d-body-dinov3) | jetjodh | [other](https://huggingface.co/facebook/sam-3d-body-dinov3/blob/main/LICENSE) | Yes | SAM License (Meta, 2025-11-19): royalty-free commercial use permitted, no revenue threshold; obligations: no reverse engineering of components, trade-control/ITAR compliance, acknowledge SAM in publications. | 3 | 1,180 | 2025-11-25 |

### LivePortrait

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Kijai/LivePortrait_safetensors](https://huggingface.co/Kijai/LivePortrait_safetensors) | Kijai | [mit](https://huggingface.co/spaces/KlingTeam/LivePortrait/blob/main/LICENSE) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 5 | 0 | 2024-08-02 |

### Pose

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/SDPose](https://huggingface.co/Comfy-Org/SDPose) | Comfy-Org | [mit](https://spdx.org/licenses/MIT.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 29,734 | 2026-08-17 |
| [Kijai/vitpose_comfy](https://huggingface.co/Kijai/vitpose_comfy) | Kijai | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 0 | 2025-09-23 |
| [hr16/DWPose-TorchScript-BatchSize5](https://huggingface.co/hr16/DWPose-TorchScript-BatchSize5) | hr16 | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 0 | 2023-11-30 |
| [yzd-v/DWPose](https://huggingface.co/yzd-v/DWPose) | yzd-v | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 0 | 2023-08-22 |

### PoseStudio

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [MIUProject/VNCCS_PoseStudio](https://huggingface.co/MIUProject/VNCCS_PoseStudio) | MIUProject | [mit](https://spdx.org/licenses/MIT.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 0 | 2026-05-23 |
| [MIUProject/VNCCS_PoseStudio_Klein](https://huggingface.co/MIUProject/VNCCS_PoseStudio_Klein) | MIUProject | [mit](https://spdx.org/licenses/MIT.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 0 | 2026-07-21 |

### Audio

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Kijai/MelBandRoFormer_comfy](https://huggingface.co/Kijai/MelBandRoFormer_comfy) | Kijai | [mit](https://huggingface.co/KimberleyJSN/melbandroformer/blob/main/README.md) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 95,238 | 2025-08-23 |
| [Kijai/wav2vec2_safetensors](https://huggingface.co/Kijai/wav2vec2_safetensors) | Kijai | [mit](https://spdx.org/licenses/MIT.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 3 | 0 | 2025-08-25 |

### Anima

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [circlestone-labs/Anima](https://huggingface.co/circlestone-labs/Anima) | circlestone-labs | [other](https://huggingface.co/circlestone-labs/Anima/raw/main/LICENSE.md) | No | CircleStone Labs Non-Commercial License v1.2: model & derivatives non-commercial, non-production; generated images (Outputs) may be used commercially; commercial model use requires a separate license (circlestone.ai); derivative of Cosmos-Predict2-2B - NVIDIA Open Model License applies to derivatives. | 2 | 816,639 | 2026-07-24 |
| [kohya-ss/Anima-LLLite](https://huggingface.co/kohya-ss/Anima-LLLite) | kohya-ss | [other](https://huggingface.co/kohya-ss/Anima-LLLite/raw/main/LICENSE) | No | CircleStone Labs Non-Commercial License v1.0 (same as Anima base): model & derivatives non-commercial, non-production; generated images (Outputs) may be used commercially; commercial model use requires a separate license (circlestone.ai). | 1 | 0 | 2026-08-02 |

### Kaloscope

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [heathcliff01/Kaloscope](https://huggingface.co/heathcliff01/Kaloscope) | heathcliff01 | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2 | 0 | 2025-10-20 |

### Alissonerdx

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Alissonerdx/BFS-Best-Face-Swap](https://huggingface.co/Alissonerdx/BFS-Best-Face-Swap) | Alissonerdx | [mit](https://spdx.org/licenses/MIT.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 121,693 | 2026-08-10 |

### Bingsu

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Bingsu/adetailer](https://huggingface.co/Bingsu/adetailer) | Bingsu | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 10,484,126 | 2024-11-21 |

### ChenkinNoob

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [ChenkinNoob/Chenkin-UniControl-XL](https://huggingface.co/ChenkinNoob/Chenkin-UniControl-XL) | ChenkinNoob | [fair-ai-public-license-1.0-sd](https://freedevproject.org/faipl-1.0-sd/) | No | Fair AI Public License 1.0 SD (FAIPL) - non-commercial use only. | 1 | 981 | 2026-04-10 |
| [ChenkinNoob/ChenkinNoob-XL-V0.5](https://huggingface.co/ChenkinNoob/ChenkinNoob-XL-V0.5) | ChenkinNoob | [other](https://freedevproject.org/faipl-1.0-sd/) | No | Fair AI Public License 1.0 SD (FAIPL) - non-commercial use only (same as base model Chenkin-UniControl-XL). | 1 | 35 | 2026-04-10 |

### Comfy-Org

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3) | Comfy-Org | [other](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE) | Conditional | MiniMax H3 Community License (2026-08-02): free commercial use below US$20M yearly revenue; >=US$20M requires prior written authorization (api@minimax.io); territory excludes EU/UK/South Korea/USA; must display 'MiniMax H3' on commercial product UI; AUP applies. | 3 | 14,015,769 | 2026-08-17 |
| [Comfy-Org/OneReward_repackaged](https://huggingface.co/Comfy-Org/OneReward_repackaged) | Comfy-Org | [cc-by-nc-4.0](https://spdx.org/licenses/CC-BY-NC-4.0.html) | No | Non-commercial license: free use excludes commercial rights; commercial use requires a purchased license. | 1 | 8,164 | 2026-08-17 |
| [Comfy-Org/mediapipe](https://huggingface.co/Comfy-Org/mediapipe) | Comfy-Org | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 5,013 | 2026-08-17 |

### Kijai

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Kijai/MiniMax-H3-TAE](https://huggingface.co/Kijai/MiniMax-H3-TAE) | Kijai | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 0 | 2026-08-05 |
| [Kijai/MiniMax-H3-experimental](https://huggingface.co/Kijai/MiniMax-H3-experimental) | Kijai | - | Review | Custom or undeclared license; commercial conditions require human review of the license text. | 1 | 0 | 2026-08-08 |

### Kim2091

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [Kim2091/AnimeSharp](https://huggingface.co/Kim2091/AnimeSharp) | Kim2091 | [cc-by-nc-sa-4.0](https://spdx.org/licenses/CC-BY-NC-SA-4.0.html) | No | CC BY-NC-SA 4.0: non-commercial use only; attribution + share-alike required; commercial use needs separate permission from the author. | 1 | 0 | 2024-12-08 |

### LBH-123-AI

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [LBH-123-AI/Minimax_h3_latent_Upscaler](https://huggingface.co/LBH-123-AI/Minimax_h3_latent_Upscaler) | LBH-123-AI | - | Review | Custom or undeclared license; commercial conditions require human review of the license text. | 1 | 0 | 2026-08-17 |

### apple

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [apple/Sharp](https://huggingface.co/apple/Sharp) | apple | [apple-amlr](https://github.com/apple/ml-sharp/blob/main/LICENSE) | Review | Apple Sample Code license (apple-amlr) - personal, non-exclusive use; commercial redistribution subject to Apple's terms, review required. | 1 | 2,715 | 2025-12-18 |

### lrzjason

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [lrzjason/Anything2Real_2601](https://huggingface.co/lrzjason/Anything2Real_2601) | lrzjason | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 1 | 164,231 | 2026-01-28 |

### mashb1t

| Model | Provider | License | Commercial | Commercial terms | Files | Downloads | Updated |
| :--- | :--- | :--- | :---: | :--- | ---: | ---: | :--- |
| [mashb1t/misc](https://huggingface.co/mashb1t/misc) | mashb1t | [apache-2.0](https://github.com/facebookresearch/segment-anything/blob/main/LICENSE) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 3 | 0 | 2024-06-16 |

### Base model declarations (for derivative tracing)

> Original models that derivatives trace up to. Marked per each model's own declaration.

| Base model | Provider | License | Commercial | Commercial terms | Updated |
| :--- | :--- | :--- | :---: | :--- | :--- |
| [Qwen/Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2025-08-18 |
| [Qwen/Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2025-12-23 |
| [Qwen/Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) | Qwen | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2025-04-06 |
| [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | Qwen | [apache-2.0](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2025-07-26 |
| [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | Qwen | [apache-2.0](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2026-03-02 |
| [Wan-AI/Wan2.1-T2V-14B](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B) | Wan-AI | [apache-2.0](https://spdx.org/licenses/Apache-2.0.html) | Yes | Permissive open-source license (e.g. Apache-2.0/MIT); commercial use permitted without additional conditions. | 2025-03-12 |
| [google/gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it) | google | [gemma](https://ai.google.dev/gemma/terms) | Review | Google Gemma Terms of Use govern (not OSI open source); commercial use permitted subject to those terms. | 2025-03-21 |

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

GitHub -> **Actions** -> *Update Model Licenses* -> **Run workflow**. Also runs automatically every hour (minute 0); runs that find no license/data changes commit nothing.

## Downstream compliance integration

`data/model_license_map.json` is keyed by local filename. Look up a generation's `Base Model` value (e.g. `wan2.1_14B_SCAIL_2_fp8_scaled.safetensors`) to get its `license`. For derivative files, `derivative=true` and the `base_model` / `base_license` fields show the upstream association.

## ⚠️ Disclaimer

The **Commercial** column and the lookup map are **automated heuristics, not legal advice**:

- `Yes` - repo declares a well-known permissive SPDX id (e.g. `apache-2.0`, `mit`).
- `No` - license text contains a non-commercial restriction.
- `Conditional` - commercial use is permitted when stated conditions are met (e.g. Krea-2 below US$1M / LTX-2 below US$10M company-wide annual revenue); above the threshold a purchased/commercial license is required.
- `Review` - anything else (custom, RAIL, community, repackaged, or derivative). **Always read the actual license** before commercial use.
- **Commercial terms** - the exact commercial conditions are stated per row (e.g. Krea-2's free-commercial-below-US$1M threshold, LTX-2's US$10M threshold, or purchased-license requirements). Conditional-commercial licenses are flagged `Conditional` and the conditions are shown in the table, `licenses_output.json`, and `model_license_map.json` for audit.

Repackaged / community re-upload repos may not redeclare the original model's license; the original author's terms still apply. License terms can change. Always verify against the upstream model card. No warranty, no liability.

## License

The scripts and tooling in this repository are released under the **MIT License**. The model license metadata recorded here belongs to the respective model authors.
