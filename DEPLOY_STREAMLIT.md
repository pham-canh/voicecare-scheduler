# Deploy Streamlit Cloud — VoiceCare (free, no card needed)

Streamlit Community Cloud free: public app, deployed from a GitHub repo.

## You do (10 minutes)

1. Create a new public GitHub repo, e.g. `voicecare-scheduler`: https://github.com/new
2. Push the code (run inside the export folder — NEVER push `work/.assemblyai_key`):
   ```bash
   git remote add origin https://github.com/<user>/voicecare-scheduler.git
   git branch -M main && git push -u origin main
   ```
   Required: `app_streamlit.py`, `src/`, `requirements-streamlit.txt` (renamed to `requirements.txt` in the deploy repo).
3. Open https://share.streamlit.io → **New app** → pick repo/branch/`app_streamlit.py` → **Deploy**.
4. App → Settings → Secrets, add (NEBIUS key is what makes the NLU real):
   ```toml
   NEBIUS_API_KEY = "paste-your-key"
   GEMINI_API_KEY = "paste-your-key"
   ASSEMBLYAI_API_KEY = "paste-your-key"
   ```
   Without `NEBIUS_API_KEY` the app silently falls back to Gemini, then regex — the status bar and the Technical panel say so, but judges score the Nemotron path, so set it.
5. Verify in an incognito window: press RUN FULL DEMO → open the Technical panel → the line must read `NLU: nemotron`. If it reads `gemini`, the Nebius secret is missing — fix Secrets and redeploy.

## After you have the URL
Tell the agent: fill in the config + verify `submit --check --live-check <url>` → shoot the video opening the real URL.
