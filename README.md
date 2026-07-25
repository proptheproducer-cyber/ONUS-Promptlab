# ⚡ ONUS PromptLab

**Build · Store · Fuse · Score · Generate**

> 🔗 **Live:** [promptgeniusv0103.netlify.app](https://promptgeniusv0103.netlify.app/)

ONUS PromptLab is a single-file web app for creating, organizing, and AI-generating music prompts — optimized for [Suno](https://suno.com). It runs entirely in the browser with zero backend, zero install, and zero dependencies.

---

## What It Does

Most people using Suno wing it with vague prompts and get inconsistent results. ONUS gives you a structured workflow:

1. **Build** a library of reusable prompt blocks — lyrics, style tags, vocal direction, beat notes, arrangement cues
2. **Assemble** blocks into a master prompt using the Builder
3. **Generate** a complete song package (lyrics + style + alt styles + vocal direction) in one AI shot
4. **Score** your prompts on 8 hit criteria before you waste a generation
5. **Save** finalized master prompts and deploy them to Suno

---

## Features

| Feature | What It Does |
|---|---|
| **📚 Prompt Library** | Store, search, and filter prompts by category, tags, and rating |
| **⚡ AI Generation** | Claude generates lyrics, style tags, alt styles, vocal direction, and arrangement notes |
| **🔧 Prompt Builder** | Drag prompt blocks together into a compiled master prompt |
| **📋 Song Timeline** | Drag-and-drop song structure with section cues (verse, chorus, bridge, etc.) |
| **📊 Hit Scorecard** | Score prompts on 8 psychoacoustic criteria — hook, groove, emotion, spectral balance, novelty, and more |
| **⚡ Masters** | Save finalized multi-block prompts ready to paste into Suno |
| **🏷️ Tags System** | 100+ production tags (instruments, mood, vocals, sound design) each with full prompt descriptors |
| **📤 Import / Export** | Full JSON backup and restore — your data is always portable |
| **🕒 Version History** | Every edit saves the previous version |
| **🔒 Dev Panel** | Hidden transparency log — tap the logo 5x to open generation history |

---

## Quick Start

### Use It Online
**→ [promptgeniusv0103.netlify.app](https://promptgeniusv0103.netlify.app/)**

No install. Just open it and start building.

### Run Locally
```bash
git clone https://github.com/proptheproducer-cyber/ONUS-Promptlab.git
cd ONUS-Promptlab
open index.html   # or double-click in Finder
```

That's it. No `npm install`. No build step. One file.

---

## AI Setup

ONUS uses the [Anthropic Claude API](https://console.anthropic.com) for generation. You need your own API key.

**Get a key (free to start):**
1. Go to [console.anthropic.com](https://console.anthropic.com) → Sign up
2. API Keys → **Create Key** → copy the `sk-ant-...` key
3. In ONUS → **Create** tab → paste your key in the API Key field

**Cost:** New accounts get ~$5 free credit ≈ 200+ generations.

> **Privacy:** Your API key is stored only in your browser's `localStorage`. It's never sent anywhere except directly to Anthropic's servers when you generate.

---

## The Three Generation Engines

| Engine | Style |
|---|---|
| **V1 — ONUS** | Deep, structured — full song architecture with section-by-section direction |
| **V2 — Floss Suno Sauce** | Optimized for Suno's character limits — punchy, production-ready |
| **V3 — Prompt Genius** | Research-backed psychoacoustic approach — targets listener psychology |

Switch between engines in the Create tab to match your workflow.

---

## Data & Privacy

- All prompt data lives in your browser's `localStorage` — nothing is stored on any server
- Export your full library anytime via **📤 Export** as a JSON backup
- Clear your data anytime via browser settings or the app's reset option

---

## Folder Structure

```
ONUS-Promptlab/
├── index.html          # The entire app — this is all you need
├── Dockerfile          # For Docker/Render deployment (optional)
├── README.md
└── tools/              # Experimental Suno automation (not part of the web app)
    ├── suno_auth.py    # Playwright: capture persistent Suno login session
    ├── suno_driver.py  # Playwright: automate Suno generation via browser
    └── README.md
```

---

## Deploy Your Own

| Platform | How |
|---|---|
| **Netlify** | Drag `index.html` to [netlify.com/drop](https://app.netlify.com/drop) — live in 15 seconds |
| **Vercel** | `npx vercel --prod` from the project folder |
| **GitHub Pages** | Enable Pages in repo settings → source: `main` / root |
| **Render (Docker)** | Connect repo → Web Service → Docker → port `10000` |

---

## Version History

| Version | Notes |
|---|---|
| **v1.4** | Current — AI generation with V1/V2/V3 engines, Dev Panel, Tag Descriptors with full prompt content, Lyric Feedback Loop, Hit Scorecard |
| v1.3 | Builder, Scorecard, Timeline, Masters |
| v1.0 | Initial prompt library and storage |

---

## Built With

- Vanilla HTML / CSS / JavaScript — no frameworks, no bundler
- [Anthropic Claude API](https://anthropic.com) — AI generation
- [Suno](https://suno.com) — the music platform this is built for
