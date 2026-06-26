# Workspace Instructions & Development Guide

This workspace is set up to create short vertical (9:16, 30fps) documentary explainer video series using the custom `hearyourvoice` pipeline.

---

## 📂 Folders & Structure
Each project (defined by a `slug`) is scaffolded into:
*   `src/<slug>/` — Research briefs (`research.md`), draft scripts (`script-v1.md`), and voiceovers (`voiceover-v1.md`).
    *   `src/<slug>/edit/` — Insert plans (`ep*-insert-plan.json`) and exported timelines (`ep*-timeline.json`, `ep*-timeline.csv`).
    *   `src/<slug>/veo/` — Destination for packaged briefs (`ep*-insert-brief.json`).
*   `public/<slug>/` — Assets and generated files.
    *   `public/<slug>/voiceover/` — ElevenLabs narration MP3s.
    *   `public/<slug>/generated/` — Title/text slides and visual assets.
*   `out/<slug>/` — Destination for compiled MP4 renders.
*   `delivery/<slug>/` — The canonical delivery folder containing `manifest.json`, final videos, audio, and briefs.

---

## 🛠️ Core Scripts
The workflow uses Node scripts in the customization folder and a local Python script:

1.  **Scaffold**:
    ```bash
    node "~/.gemini/config/skills/hearyourvoice/scripts/new-project.mjs" --slug <slug> --title "<title>" --episodes <count>
    ```
2.  **Voiceover Generation** (uses ElevenLabs API):
    ```bash
    node "~/.gemini/config/skills/hearyourvoice/scripts/gen-voiceover.mjs" --slug <slug> --voice-id JBFqnCBsd6RMkjVDRZzb
    ```
3.  **Audio Measurement**:
    ```bash
    node "~/.gemini/config/skills/hearyourvoice/scripts/measure-voiceover.mjs" --dir public/<slug>/voiceover --out src/<slug>/voiceover-durations.json
    ```
4.  **Timeline Export**:
    ```bash
    node "~/.gemini/config/skills/hearyourvoice/scripts/export-timeline.mjs" --slug <slug> --episode <ep> --brief src/<slug>/edit/<ep>-insert-plan.json --durations src/<slug>/voiceover-durations.json
    ```
5.  **Stitch & Compile Video**:
    ```bash
    python3 scratch/compile_video.py --slug <slug> --episode <ep>
    ```
6.  **Package Delivery**:
    ```bash
    node "~/.gemini/config/skills/hearyourvoice/scripts/package-delivery.mjs" --slug <slug>
    ```

---

## 📋 Step-by-Step Creation Guide

For any new video project requested by the user, follow these steps:

### Step 1: Initialization & Research
1.  Run the **Scaffold** command to create files.
2.  Write a factual brief in `src/<slug>/research.md`.
3.  Draft storyboard beats in `src/<slug>/script-v1.md`.

### Step 2: Voiceover Production
1.  Format the voiceover script in `src/<slug>/voiceover-v1.md` with:
    *   `Voice id: JBFqnCBsd6RMkjVDRZzb`
    *   Short, punchy lines separated by a blank line (representing pauses).
2.  **CRITICAL**: Ask the user if the ElevenLabs image/voice generation quota is limited. If okay, run the **Voiceover Generation** script.
3.  Run the **Audio Measurement** script to extract timings to `voiceover-durations.json`. Use the `targetSec` value from the output as the master duration.

### Step 3: Insert Plan & Assets
1.  Create `src/<slug>/edit/<ep>-insert-plan.json`. Define 15-17 clips totaling exactly `targetSec` (with `0.6s` tolerance).
2.  For text slides, specify `"file": "text"` and a list of lines in the `"text_lines"` field, e.g.:
    ```json
    {
      "start_sec": 0,
      "end_sec": 6.0,
      "source": "graphic",
      "file": "text",
      "text_lines": ["Line 1", "Line 2", "Line 3"]
    }
    ```
3.  For image assets:
    *   **If the image generation quota is NOT limited**: generate assets.
    *   **If the image generation quota IS limited**: reuse assets from other folders (e.g. `public/history-ai-math-to-model/generated/`). Copy them into `public/<slug>/generated/` and prefix them with their global clip index (e.g. `2_walter_pitts_chalkboard.jpg` for Clip 2).
4.  Run the **Timeline Export** script.

### Step 4: Compilation & Delivery
1.  Run the **Stitch & Compile Video** script to compile the final `.mp4` video.
2.  Copy deliverables into place:
    *   Copy `out/<slug>/<ep>.mp4` to `out/<slug>-<ep>.mp4` (or prefix it so `package-delivery.mjs` can scan it in the root `out/` folder).
    *   Copy `src/<slug>/edit/<ep>-insert-plan.json` to `src/<slug>/veo/<ep>-insert-brief.json`.
3.  Run the **Package Delivery** script.
4.  Launch the final MP4 for the user to review.
