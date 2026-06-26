# AI Voice Explainer Video Pipeline

This workspace is set up to generate, script, compile, and package short vertical (9:16, 30fps) documentary explainer videos using the `hearyourvoice` pipeline.

---

## 📂 Project Structures
*   `src/` — Contains research, script drafts, and edit timelines for each video series.
*   `public/` — Contains generated narration audio (ElevenLabs) and image/text assets.
*   `out/` — Compiled MP4 video renders.
*   `delivery/` — Final packaged folders containing full assets and the `manifest.json`.

---

## 🛠️ Step-by-Step Creation & Compilation Guide

Here is the exact sequence of commands to run for creating a new video series:

### Step 1: Scaffold a New Project
Initializes the directories and placeholder files for a project:
```bash
node "/Users/anusornchaikaew/.gemini/config/skills/hearyourvoice/scripts/new-project.mjs" --slug <project-slug> --title "<Project Display Title>" --episodes <count>
```

### Step 2: Generate Voiceovers
After writing your scripts in `src/<project-slug>/voiceover-v1.md`, run:
```bash
node "/Users/anusornchaikaew/.gemini/config/skills/hearyourvoice/scripts/gen-voiceover.mjs" --slug <project-slug> --voice-id JBFqnCBsd6RMkjVDRZzb
```

### Step 3: Measure Audio Durations
Extracts timings from the narration MP3s and writes them to `voiceover-durations.json`:
```bash
node "/Users/anusornchaikaew/.gemini/config/skills/hearyourvoice/scripts/measure-voiceover.mjs" --dir "/Users/anusornchaikaew/Work/Train/AI_voice/public/<project-slug>/voiceover" --out "/Users/anusornchaikaew/Work/Train/AI_voice/src/<project-slug>/voiceover-durations.json"
```

### Step 4: Export Timeline
After creating your visual mapping brief in `src/<project-slug>/edit/ep1-insert-plan.json`, export the contiguous NLE timeline:
```bash
node "/Users/anusornchaikaew/.gemini/config/skills/hearyourvoice/scripts/export-timeline.mjs" --slug <project-slug> --episode ep1 --brief "/Users/anusornchaikaew/Work/Train/AI_voice/src/<project-slug>/edit/ep1-insert-plan.json" --durations "/Users/anusornchaikaew/Work/Train/AI_voice/src/<project-slug>/voiceover-durations.json"
```

### Step 5: Compile Video
Stitches visual assets, generates text slides dynamically, pads audio with silence, and outputs the final MP4:
```bash
python3 "/Users/anusornchaikaew/Work/Train/AI_voice/scratch/compile_video.py" --slug <project-slug> --episode ep1
```

### Step 6: Package Delivery
Copies the final assets (briefs, audio, videos) and generates the delivery `manifest.json`:
```bash
# 1. Copy compiled video into the main out/ folder
cp "/Users/anusornchaikaew/Work/Train/AI_voice/out/<project-slug>/ep1.mp4" "/Users/anusornchaikaew/Work/Train/AI_voice/out/<project-slug>-ep01.mp4"

# 2. Copy the insert plan to the veo/ folder
cp "/Users/anusornchaikaew/Work/Train/AI_voice/src/<project-slug>/edit/ep1-insert-plan.json" "/Users/anusornchaikaew/Work/Train/AI_voice/src/<project-slug>/veo/ep1-insert-brief.json"

# 3. Package
node "/Users/anusornchaikaew/.gemini/config/skills/hearyourvoice/scripts/package-delivery.mjs" --slug <project-slug>
```

---

## 🤖 AI Agent Integration
The folder `.agents/AGENTS.md` contains system instructions that any future AI agent will automatically load when opening this workspace. This guarantees they will follow the exact same steps, scripts, and naming conventions for any future series you request.
