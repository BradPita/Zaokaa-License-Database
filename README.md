# Zaokaa License Database

An auto-updated lookup table of **open-source / open-weight model licenses** for the models used by a ComfyUI-based generation pipeline - what license each model ships under, plus a best-effort commercial-use flag and **derivative-to-base-model tracing**.

The model inventory is extracted from the pipeline's own model manifest (`model_checker.py`), so it tracks the **real** models in production - Wan2.2, FLUX.2, Krea-2, Qwen-Image, Qwen3-TTS, LTX-2.3, Z-Image, Bernini-R, SCAIL-2, and more. Distribution-brand references are scrubbed from the public data.

The `data/model_license_map.json` artifact feeds a downstream compliance tool: it maps each local model file to its license (for filling the license column of a generation compliance log from the `Base Model` filename).

## How it works

1. `scripts/extract_manifest.py` - reads a `model_checker.py`-style manifest and writes `data/models_manifest.json` (local filename -> Hugging Face repo; distribution-brand entries scrubbed). Re-run when the pipeline's model set changes.
2. `scripts/fetch_licenses.py` - queries the <a href="https://huggingface.co/docs/huggingface_hub" target="_blank" rel="noopener noreferrer">Hugging Face Hub REST API</a> for each unique repo's `cardData.license` -> `data/licenses_output.csv` + `.json` (one row per repo, including base models).
3. `scripts/build_lookup.py` - joins the manifest + licenses + `data/base_models.json` -> `data/model_license_map.json` (filename -> license, with derivative tracing).
4. `scripts/generate_readme.py` - renders the table below.
5. `.github/workflows/update_licenses.yml` - re-runs steps 2–4 weekly and auto-commits results.

No web scraping, no API key required for public metadata. Pure stdlib Python.

## Derivative model policy

Files whose name contains a **derivative marker** - `nsfw`, `abliterated`, `remix`, `rapid`, `aio`, `merge`, `finetune` - are **downgraded to `Review`**, because a community merge/finetune may mix in non-commercial components even when the base is permissive.

Each derivative is **traced up to its original base model** (registry in `data/base_models.json`), so the association is queryable. The **base model is marked according to its own declaration** on its original HF repo. So a derivative entry carries both its (downgraded) review status and the base model's original license.

## License table

<!-- LICENSE_TABLE_START -->
_Last updated: 2026-08-01 14:41 UTC · 59 tracked repos + 7 base models_

## Tracked models

### Wan

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged" target="_blank" rel="noopener noreferrer">Comfy-​Org/​Wan_2.1_ComfyUI_repackaged</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://huggingface.co/Wan-AI/Wan2.1-T2V-14B" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">3</td>
<td align="right">2,198,113</td>
<td align="left">2026-01-28</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged" target="_blank" rel="noopener noreferrer">Comfy-​Org/​Wan_2.2_ComfyUI_Repackaged</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://huggingface.co/Wan-AI/Wan2.2-Animate-14B" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">5,284,364</td>
<td align="left">2026-07-03</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/FX-FeiHou/wan2.2-Remix" target="_blank" rel="noopener noreferrer">FX-​FeiHou/​wan2.2-​Remix</a></td>
<td align="left">FX-FeiHou</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">1</td>
<td align="right">2</td>
<td align="left">2026-03-24</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Kijai/WanVideo_comfy" target="_blank" rel="noopener noreferrer">Kijai/​WanVideo_comfy</a></td>
<td align="left">Kijai</td>
<td align="left"><a href="https://huggingface.co/Wan-AI/Wan2.1-T2V-14B" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">5</td>
<td align="right">1,834,935</td>
<td align="left">2026-06-13</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Wan-AI/Wan2.2-Animate-14B" target="_blank" rel="noopener noreferrer">Wan-​AI/​Wan2.2-​Animate-​14B</a></td>
<td align="left">Wan-AI</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">20,293</td>
<td align="left">2025-11-05</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/rzgar/NSFW-Wan-UMT5-XXL-V2" target="_blank" rel="noopener noreferrer">rzgar/​NSFW-​Wan-​UMT5-​XXL-​V2</a></td>
<td align="left">rzgar</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">163</td>
<td align="left">2026-07-17</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/rzgar/Wan2.2_I2V_LightX2V_2Step" target="_blank" rel="noopener noreferrer">rzgar/​Wan2.2_I2V_LightX2V_2Step</a></td>
<td align="left">rzgar</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">1,315</td>
<td align="left">2026-07-17</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/spacepxl/Wan2.1-VAE-upscale2x" target="_blank" rel="noopener noreferrer">spacepxl/​Wan2.1-​VAE-​upscale2x</a></td>
<td align="left">spacepxl</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">49,026</td>
<td align="left">2025-10-26</td>
</tr>
</tbody>
</table>

### FLUX

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/silveroxides/FLUX.2-dev-fp8_scaled" target="_blank" rel="noopener noreferrer">silveroxides/​FLUX.2-​dev-​fp8_scaled</a></td>
<td align="left">silveroxides</td>
<td align="left"><a href="https://huggingface.co/black-forest-labs/FLUX.2-dev/blob/main/LICENSE.md" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">1</td>
<td align="right">16,114</td>
<td align="left">2026-07-15</td>
</tr>
</tbody>
</table>

### Krea

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/Krea-2" target="_blank" rel="noopener noreferrer">Comfy-​Org/​Krea-​2</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://cdn.jsdelivr.net/gh/krea-ai/krea-2@db3984fbc6e13b34c0064990fc2d95ac64d00058/assets/hf_samples/LICENSE.pdf" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">No</td>
<td align="right">3</td>
<td align="right">10</td>
<td align="left">2026-07-20</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/conradlocke/krea2-identity-edit" target="_blank" rel="noopener noreferrer">conradlocke/​krea2-​identity-​edit</a></td>
<td align="left">conradlocke</td>
<td align="left"><a href="https://cdn.jsdelivr.net/gh/krea-ai/krea-2@db3984fbc6e13b34c0064990fc2d95ac64d00058/assets/hf_samples/LICENSE.pdf" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">No</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2026-07-29</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/uzumix/krea2filterbypass3.safetensors" target="_blank" rel="noopener noreferrer">uzumix/​krea2filterbypass3.safetensors</a></td>
<td align="left">uzumix</td>
<td align="left"><a href="https://cdn.jsdelivr.net/gh/krea-ai/krea-2@db3984fbc6e13b34c0064990fc2d95ac64d00058/assets/hf_samples/LICENSE.pdf" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">No</td>
<td align="right">1</td>
<td align="right">4,130</td>
<td align="left">2026-07-08</td>
</tr>
</tbody>
</table>

### Qwen-Image

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI" target="_blank" rel="noopener noreferrer">Comfy-​Org/​Qwen-​Image-​Edit_ComfyUI</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">821,932</td>
<td align="left">2026-07-01</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI" target="_blank" rel="noopener noreferrer">Comfy-​Org/​Qwen-​Image_ComfyUI</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">1,846,848</td>
<td align="left">2026-06-06</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO" target="_blank" rel="noopener noreferrer">Phr00t/​Qwen-​Image-​Edit-​Rapid-​AIO</a></td>
<td align="left">Phr00t</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2026-02-03</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511" target="_blank" rel="noopener noreferrer">QuantFunc/​Nunchaku-​Qwen-​Image-​EDIT-​2511</a></td>
<td align="left">QuantFunc</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">4,418</td>
<td align="left">2026-06-19</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA" target="_blank" rel="noopener noreferrer">fal/​Qwen-​Image-​Edit-​2511-​Multiple-​Angles-​LoRA</a></td>
<td align="left">fal</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">62,244</td>
<td align="left">2026-01-07</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/lightx2v/Qwen-Image-2512-Lightning" target="_blank" rel="noopener noreferrer">lightx2v/​Qwen-​Image-​2512-​Lightning</a></td>
<td align="left">lightx2v</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">70,227</td>
<td align="left">2026-01-15</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning" target="_blank" rel="noopener noreferrer">lightx2v/​Qwen-​Image-​Edit-​2511-​Lightning</a></td>
<td align="left">lightx2v</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">289,282</td>
<td align="left">2026-01-15</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/lrzjason/QwenEdit_Consistance_Edit" target="_blank" rel="noopener noreferrer">lrzjason/​QwenEdit_Consistance_Edit</a></td>
<td align="left">lrzjason</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2026-04-17</td>
</tr>
</tbody>
</table>

### Qwen-TTS

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base" target="_blank" rel="noopener noreferrer">Qwen/​Qwen3-​TTS-​12Hz-​0.6B-​Base</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">12</td>
<td align="right">421,115</td>
<td align="left">2026-01-29</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice" target="_blank" rel="noopener noreferrer">Qwen/​Qwen3-​TTS-​12Hz-​0.6B-​CustomVoice</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">12</td>
<td align="right">1,603,747</td>
<td align="left">2026-01-29</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base" target="_blank" rel="noopener noreferrer">Qwen/​Qwen3-​TTS-​12Hz-​1.7B-​Base</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">12</td>
<td align="right">2,447,986</td>
<td align="left">2026-01-23</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice" target="_blank" rel="noopener noreferrer">Qwen/​Qwen3-​TTS-​12Hz-​1.7B-​CustomVoice</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">12</td>
<td align="right">2,400,018</td>
<td align="left">2026-01-29</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign" target="_blank" rel="noopener noreferrer">Qwen/​Qwen3-​TTS-​12Hz-​1.7B-​VoiceDesign</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">12</td>
<td align="right">626,206</td>
<td align="left">2026-01-29</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3-TTS-Tokenizer-12Hz" target="_blank" rel="noopener noreferrer">Qwen/​Qwen3-​TTS-​Tokenizer-​12Hz</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">4</td>
<td align="right">108,824</td>
<td align="left">2026-01-29</td>
</tr>
</tbody>
</table>

### Qwen3-LLM

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/mradermacher/Huihui-Qwen3.5-9B-abliterated-GGUF" target="_blank" rel="noopener noreferrer">mradermacher/​Huihui-​Qwen3.5-​9B-​abliterated-​GGUF</a></td>
<td align="left">mradermacher</td>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">15,844</td>
<td align="left">2026-03-10</td>
</tr>
</tbody>
</table>

### LTX-Video

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/ltx-2" target="_blank" rel="noopener noreferrer">Comfy-​Org/​ltx-​2</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://github.com/Lightricks/LTX-2/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">2</td>
<td align="right">0</td>
<td align="left">2026-03-08</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Kijai/LTX2.3_comfy" target="_blank" rel="noopener noreferrer">Kijai/​LTX2.3_comfy</a></td>
<td align="left">Kijai</td>
<td align="left"><a href="https://github.com/Lightricks/LTX-2/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">6</td>
<td align="right">979,712</td>
<td align="left">2026-07-28</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Lightricks/LTX-2.3" target="_blank" rel="noopener noreferrer">Lightricks/​LTX-​2.3</a></td>
<td align="left">Lightricks</td>
<td align="left"><a href="https://github.com/Lightricks/LTX-2/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">1</td>
<td align="right">2,128,047</td>
<td align="left">2026-07-09</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/joyfox/LTX2.3-ICEdit-Insight" target="_blank" rel="noopener noreferrer">joyfox/​LTX2.3-​ICEdit-​Insight</a></td>
<td align="left">joyfox</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">4</td>
<td align="right">62,815</td>
<td align="left">2026-07-23</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint" target="_blank" rel="noopener noreferrer">oumoumad/​LTX-​2.3-​22b-​IC-​LoRA-​Outpaint</a></td>
<td align="left">oumoumad</td>
<td align="left"><a href="https://github.com/Lightricks/LTX-2/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2026-04-10</td>
</tr>
</tbody>
</table>

### Z-Image

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/z_image_turbo" target="_blank" rel="noopener noreferrer">Comfy-​Org/​z_image_turbo</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">5,218,592</td>
<td align="left">2026-07-02</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1" target="_blank" rel="noopener noreferrer">alibaba-​pai/​Z-​Image-​Turbo-​Fun-​Controlnet-​Union-​2.1</a></td>
<td align="left">alibaba-pai</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">75,682</td>
<td align="left">2026-02-26</td>
</tr>
</tbody>
</table>

### Bernini

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/Bernini-R" target="_blank" rel="noopener noreferrer">Comfy-​Org/​Bernini-​R</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">0</td>
<td align="left">2026-06-30</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/rzgar/Bernini-R-LightX2V-4step-loras" target="_blank" rel="noopener noreferrer">rzgar/​Bernini-​R-​LightX2V-​4step-​loras</a></td>
<td align="left">rzgar</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">18,947</td>
<td align="left">2026-07-02</td>
</tr>
</tbody>
</table>

### SCAIL

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/SCAIL-2" target="_blank" rel="noopener noreferrer">Comfy-​Org/​SCAIL-​2</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://spdx.org/licenses/MIT.html" target="_blank" rel="noopener noreferrer">mit</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">0</td>
<td align="left">2026-07-15</td>
</tr>
</tbody>
</table>

### SeedVR

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/numz/SeedVR2_comfyUI" target="_blank" rel="noopener noreferrer">numz/​SeedVR2_comfyUI</a></td>
<td align="left">numz</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">212,750</td>
<td align="left">2025-11-09</td>
</tr>
</tbody>
</table>

### Segment Anything

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/sam3.1" target="_blank" rel="noopener noreferrer">Comfy-​Org/​sam3.1</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://github.com/facebookresearch/sam3/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2026-05-06</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/jetjodh/sam-3d-body-dinov3" target="_blank" rel="noopener noreferrer">jetjodh/​sam-​3d-​body-​dinov3</a></td>
<td align="left">jetjodh</td>
<td align="left"><a href="https://huggingface.co/facebook/sam-3d-body-dinov3/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">3</td>
<td align="right">1,206</td>
<td align="left">2025-11-25</td>
</tr>
</tbody>
</table>

### LivePortrait

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Kijai/LivePortrait_safetensors" target="_blank" rel="noopener noreferrer">Kijai/​LivePortrait_safetensors</a></td>
<td align="left">Kijai</td>
<td align="left"><a href="https://huggingface.co/spaces/KlingTeam/LivePortrait/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">mit</a></td>
<td align="center">Yes</td>
<td align="right">5</td>
<td align="right">0</td>
<td align="left">2024-08-02</td>
</tr>
</tbody>
</table>

### Pose

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Comfy-Org/SDPose" target="_blank" rel="noopener noreferrer">Comfy-​Org/​SDPose</a></td>
<td align="left">Comfy-Org</td>
<td align="left"><a href="https://spdx.org/licenses/MIT.html" target="_blank" rel="noopener noreferrer">mit</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">25,259</td>
<td align="left">2026-03-03</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Kijai/vitpose_comfy" target="_blank" rel="noopener noreferrer">Kijai/​vitpose_comfy</a></td>
<td align="left">Kijai</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">0</td>
<td align="left">2025-09-23</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/hr16/DWPose-TorchScript-BatchSize5" target="_blank" rel="noopener noreferrer">hr16/​DWPose-​TorchScript-​BatchSize5</a></td>
<td align="left">hr16</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2023-11-30</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/yzd-v/DWPose" target="_blank" rel="noopener noreferrer">yzd-​v/​DWPose</a></td>
<td align="left">yzd-v</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2023-08-22</td>
</tr>
</tbody>
</table>

### PoseStudio

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/MIUProject/VNCCS_PoseStudio" target="_blank" rel="noopener noreferrer">MIUProject/​VNCCS_PoseStudio</a></td>
<td align="left">MIUProject</td>
<td align="left"><a href="https://spdx.org/licenses/MIT.html" target="_blank" rel="noopener noreferrer">mit</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2026-05-23</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/MIUProject/VNCCS_PoseStudio_Klein" target="_blank" rel="noopener noreferrer">MIUProject/​VNCCS_PoseStudio_Klein</a></td>
<td align="left">MIUProject</td>
<td align="left"><a href="https://spdx.org/licenses/MIT.html" target="_blank" rel="noopener noreferrer">mit</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2026-07-21</td>
</tr>
</tbody>
</table>

### Audio

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Kijai/MelBandRoFormer_comfy" target="_blank" rel="noopener noreferrer">Kijai/​MelBandRoFormer_comfy</a></td>
<td align="left">Kijai</td>
<td align="left"><a href="https://huggingface.co/KimberleyJSN/melbandroformer/blob/main/README.md" target="_blank" rel="noopener noreferrer">mit</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">93,004</td>
<td align="left">2025-08-23</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Kijai/wav2vec2_safetensors" target="_blank" rel="noopener noreferrer">Kijai/​wav2vec2_safetensors</a></td>
<td align="left">Kijai</td>
<td align="left"><a href="https://spdx.org/licenses/MIT.html" target="_blank" rel="noopener noreferrer">mit</a></td>
<td align="center">Yes</td>
<td align="right">3</td>
<td align="right">0</td>
<td align="left">2025-08-25</td>
</tr>
</tbody>
</table>

### Anima

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/circlestone-labs/Anima" target="_blank" rel="noopener noreferrer">circlestone-​labs/​Anima</a></td>
<td align="left">circlestone-labs</td>
<td align="left"><a href="LICENSE.md" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">2</td>
<td align="right">843,139</td>
<td align="left">2026-07-24</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/kohya-ss/Anima-LLLite" target="_blank" rel="noopener noreferrer">kohya-​ss/​Anima-​LLLite</a></td>
<td align="left">kohya-ss</td>
<td align="left"><a href="LICENSE" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2026-05-20</td>
</tr>
</tbody>
</table>

### Kaloscope

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/heathcliff01/Kaloscope" target="_blank" rel="noopener noreferrer">heathcliff01/​Kaloscope</a></td>
<td align="left">heathcliff01</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">2</td>
<td align="right">0</td>
<td align="left">2025-10-20</td>
</tr>
</tbody>
</table>

### Bingsu

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Bingsu/adetailer" target="_blank" rel="noopener noreferrer">Bingsu/​adetailer</a></td>
<td align="left">Bingsu</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">10,272,979</td>
<td align="left">2024-11-21</td>
</tr>
</tbody>
</table>

### ChenkinNoob

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/ChenkinNoob/Chenkin-UniControl-XL" target="_blank" rel="noopener noreferrer">ChenkinNoob/​Chenkin-​UniControl-​XL</a></td>
<td align="left">ChenkinNoob</td>
<td align="left"><a href="https://freedevproject.org/faipl-1.0-sd/" target="_blank" rel="noopener noreferrer">fair-​ai-​public-​license-​1.0-​sd</a></td>
<td align="center">No</td>
<td align="right">1</td>
<td align="right">812</td>
<td align="left">2026-04-10</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/ChenkinNoob/ChenkinNoob-XL-V0.5" target="_blank" rel="noopener noreferrer">ChenkinNoob/​ChenkinNoob-​XL-​V0.5</a></td>
<td align="left">ChenkinNoob</td>
<td align="left"><a href="https://freedevproject.org/faipl-1.0-sd/" target="_blank" rel="noopener noreferrer">other</a></td>
<td align="center">Review</td>
<td align="right">1</td>
<td align="right">35</td>
<td align="left">2026-04-10</td>
</tr>
</tbody>
</table>

### Kim2091

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Kim2091/AnimeSharp" target="_blank" rel="noopener noreferrer">Kim2091/​AnimeSharp</a></td>
<td align="left">Kim2091</td>
<td align="left"><a href="https://spdx.org/licenses/CC-BY-NC-SA-4.0.html" target="_blank" rel="noopener noreferrer">cc-​by-​nc-​sa-​4.0</a></td>
<td align="center">No</td>
<td align="right">1</td>
<td align="right">0</td>
<td align="left">2024-12-08</td>
</tr>
</tbody>
</table>

### apple

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/apple/Sharp" target="_blank" rel="noopener noreferrer">apple/​Sharp</a></td>
<td align="left">apple</td>
<td align="left"><a href="https://github.com/apple/ml-sharp/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">apple-​amlr</a></td>
<td align="center">Review</td>
<td align="right">1</td>
<td align="right">3,306</td>
<td align="left">2025-12-18</td>
</tr>
</tbody>
</table>

### lrzjason

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/lrzjason/Anything2Real_2601" target="_blank" rel="noopener noreferrer">lrzjason/​Anything2Real_2601</a></td>
<td align="left">lrzjason</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">1</td>
<td align="right">117,333</td>
<td align="left">2026-01-28</td>
</tr>
</tbody>
</table>

### mashb1t

<table>
<colgroup>
<col width="30%">
<col width="9%">
<col width="20%">
<col width="10%">
<col width="6%">
<col width="8%">
<col width="17%">
</colgroup>
<thead>
<tr>
<th align="left">Model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="right">Files</th>
<th align="right">Downloads</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/mashb1t/misc" target="_blank" rel="noopener noreferrer">mashb1t/​misc</a></td>
<td align="left">mashb1t</td>
<td align="left"><a href="https://github.com/facebookresearch/segment-anything/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="right">3</td>
<td align="right">0</td>
<td align="left">2024-06-16</td>
</tr>
</tbody>
</table>

### Base model declarations (for derivative tracing)

> Original models that derivatives trace up to. Marked per each model's own declaration.

<table>
<colgroup>
<col width="34%">
<col width="12%">
<col width="22%">
<col width="12%">
<col width="20%">
</colgroup>
<thead>
<tr>
<th align="left">Base model</th>
<th align="left">Provider</th>
<th align="left">License</th>
<th align="center">Commercial</th>
<th align="left">Updated</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen-Image" target="_blank" rel="noopener noreferrer">Qwen/​Qwen-​Image</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="left">2025-08-18</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen-Image-Edit-2511" target="_blank" rel="noopener noreferrer">Qwen/​Qwen-​Image-​Edit-​2511</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="left">2025-12-23</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct" target="_blank" rel="noopener noreferrer">Qwen/​Qwen2.5-​VL-​7B-​Instruct</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="left">2025-04-06</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3-8B" target="_blank" rel="noopener noreferrer">Qwen/​Qwen3-​8B</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="left">2025-07-26</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3.5-9B" target="_blank" rel="noopener noreferrer">Qwen/​Qwen3.5-​9B</a></td>
<td align="left">Qwen</td>
<td align="left"><a href="https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="left">2026-03-02</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/Wan-AI/Wan2.1-T2V-14B" target="_blank" rel="noopener noreferrer">Wan-​AI/​Wan2.1-​T2V-​14B</a></td>
<td align="left">Wan-AI</td>
<td align="left"><a href="https://spdx.org/licenses/Apache-2.0.html" target="_blank" rel="noopener noreferrer">apache-​2.0</a></td>
<td align="center">Yes</td>
<td align="left">2025-03-12</td>
</tr>
<tr>
<td align="left"><a href="https://huggingface.co/google/gemma-3-12b-it" target="_blank" rel="noopener noreferrer">google/​gemma-​3-​12b-​it</a></td>
<td align="left">google</td>
<td align="left"><a href="https://ai.google.dev/gemma/terms" target="_blank" rel="noopener noreferrer">gemma</a></td>
<td align="center">Review</td>
<td align="left">2025-03-21</td>
</tr>
</tbody>
</table>

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
