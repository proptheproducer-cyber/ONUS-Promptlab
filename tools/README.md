# Tools — Experimental Automation Scripts

These scripts are **not part of the ONUS PromptLab web app**. They are experimental utilities for automating Suno's web UI using [Playwright](https://playwright.dev/).

> ⚠️ **Note:** Automating Suno's web interface may violate their [Terms of Service](https://suno.com/terms). Use at your own risk and discretion.

---

## Scripts

### `suno_auth.py`
Launches a persistent Chrome profile, navigates to `suno.com/create`, and waits for you to log in manually. Once logged in, it saves the session state so `suno_driver.py` can reuse it without re-logging in.

**Setup:**
```bash
pip install playwright
playwright install chromium
```

**Run:**
```bash
python suno_auth.py
```
Log in to Suno in the browser window that opens, then close or wait — the session saves to `~/suno_automation_profile`.

---

### `suno_driver.py`
Uses the saved session from `suno_auth.py` to open Suno, switch to Custom mode, paste lyrics and a style prompt, and click Create.

**Run:**
```bash
python suno_driver.py '{"title": "My Track", "lyrics": "[Verse]\nHello world", "style": "lo-fi, chill, 85 BPM"}'
```

Or run without arguments to use the built-in test data.

---

## Dependencies
- Python 3.8+
- `playwright` (`pip install playwright && playwright install chromium`)
