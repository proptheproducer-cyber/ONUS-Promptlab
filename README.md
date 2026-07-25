# ⚡ ONUS PromptLab

**Build · Store · Fuse · Score · Deploy**

ONUS PromptLab is a single-file web app for creating, organizing, and AI-generating music prompts — optimized for [Suno](https://suno.com). It runs entirely in the browser with zero backend required.

---

## Features

- **Prompt Library** — Store and search lyrics, style tags, vocal direction, arrangement notes, beat descriptions, and more
- **AI Generation** — Describe your song and Claude generates full lyrics, style prompts, alt styles, vocal direction, and arrangement notes in one shot
- **Prompt Builder** — Assemble individual prompt blocks into a master prompt
- **Song Timeline** — Drag-and-drop song structure builder with section cues
- **Hit Scorecard** — Score prompts on 8 psychoacoustic criteria (hook memorability, groove, spectral balance, etc.)
- **Masters** — Save finalized multi-block master prompts ready to paste into Suno
- **Import / Export** — Full JSON backup and restore
- **Version History** — Every edit to a prompt saves the previous version

---

## Quick Start

### Run Locally
1. Download or clone this repo
2. Open `index.html` in any modern browser (Chrome, Safari, Firefox)
3. No server, no install, no dependencies

### Deploy Online
Drop `index.html` on any static host:
- **GitHub Pages** — Push to `main`, enable Pages in repo settings
- **Netlify** — Drag-and-drop `index.html` at app.netlify.com
- **Vercel** — `vercel --prod` or drag-and-drop

---

## AI Setup (Required for Generation)

ONUS uses the [Anthropic Claude API](https://console.anthropic.com) for AI generation.

1. Go to [console.anthropic.com](https://console.anthropic.com) → Sign up → API Keys → **Create Key**
2. Open ONUS → go to the **Create** tab
3. Paste your `sk-ant-...` key into the API Key field — it's saved locally in your browser only

> **Note:** Your API key is stored in `localStorage` in your browser and is never sent anywhere except directly to Anthropic's API. Keep your URL private if deploying publicly.

**Cost:** ~$5 free credit on signup ≈ 200+ generations.

---

## Data & Privacy

- All prompt data is stored in your browser's `localStorage` — nothing is sent to any server
- The Anthropic API key is stored locally in your browser
- Export your data anytime via the **📤 Export** button for a full JSON backup

---

## Folder Structure

```
ONUS-Promptlab/
├── index.html          # The entire app — open this in a browser
├── README.md
└── tools/              # Experimental automation scripts (not part of the web app)
    ├── suno_auth.py    # Playwright: capture Suno login session
    ├── suno_driver.py  # Playwright: automate Suno generation
    └── README.md
```

---

## Version History

| Version | Notes |
|---|---|
| v1.4 | Current — AI generation with V1 ONUS, V2 Floss Suno Sauce, V3 Prompt Genius engines; Dev Panel; Tag Descriptors; Lyric Feedback Loop |
| v1.3 | Builder, Scorecard, Timeline |
| v1.0 | Initial library + prompt storage |
