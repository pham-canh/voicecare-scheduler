# VoiceCare Scheduler — Nebius x NVIDIA Global AI Hackathon (Devpost entry)

![demo](https://img.shields.io/badge/demo-live-brightgreen) ![license](https://img.shields.io/badge/license-MIT-green)

Event: Devpost — Nebius x NVIDIA Global AI Hackathon | Stack: voice + NVIDIA Nemotron NLU | Demo: https://voicecare-scheduler-ajthuna54dqqhpqtt52n2b.streamlit.app/

**Status:** in progress. This is a separate competition from
[`assemblyai-voice-agent`](https://github.com/pham-canh/assemblyai-voice-agent),
which is the completed AssemblyAI Voice Agent Hackathon (lablab.ai) entry.

> Speak to book your clinic visit — a voice agent that books appointments for elderly patients: listen → confirm aloud → book, with per-stage latency in ms. English-only.

## Nebius x NVIDIA Global AI Hackathon (Devpost entry)

NLU runs on **NVIDIA Nemotron (`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`) via
Nebius Token Factory** on Nebius AI Cloud. Gemini stays as automatic fallback,
regex as last resort. Speech-to-text stays AssemblyAI.

```bash
export NEBIUS_API_KEY='...'   # Token Factory key (free $25 with code NEBIUS-DEVPOST-GLOBAL26)
export NEMOTRON_MODEL='nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B'  # optional override
export NEBIUS_BASE_URL='https://api.tokenfactory.nebius.com/v1'  # optional override
```

Smoke test (needs key in env):
```bash
python3 -c "import sys; sys.path.insert(0, 'src'); from agent.nemotron_client import nemotron_call; print(nemotron_call('Output JSON only: {"verdict": "yes|no|unclear"}.', 'Classify: yes please book it'))"
```

## Demo

- Live: https://voicecare-scheduler-ajthuna54dqqhpqtt52n2b.streamlit.app/ (Streamlit Cloud, judges open and use it, no setup — if asleep, press Wake)

## Run (5 minutes, no questions asked)

```bash
echo "[]" > src/bookings.json   # reset demo slots first (each typed run writes one slot)
python3 src/main.py "your test input"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest src/ -q
```

## How it works (5 business states)

```
LISTENING → UNDERSTANDING → CHECKING → CONFIRMATION → BOOKED
Patient speaks English → agent asks what's missing in English (specialty first) → read-only
slot check → patient says YES (strict, transcript-proof) → booking written + .ics
```

Booking flow: **specialty → doctor → date → time → slot check → confirm → book + reference code.** All agent lines are pure English (e.g. `Book a cardiology checkup tomorrow morning at 9`). The AI never auto-switches a full slot — it asks first. Phone is asked last, only for the confirmation message.

## Architecture

```
mic/file --token+WS--> AssemblyAI Voice Agent API (inline en session)
  |--transcript.user--> tools local (check_availability/book, YES-gated strict)
  |--reply.audio (TTS)--> patient hears | barge-in | escalation
            ||
            |fallback|--> src/main.py run_pipeline (batch/STT v3 WS + regex+tools)
                                           |-> app_streamlit.py (Patient/Assistant dialogue, EN UI)
                                           |-> app.py (Gradio HF Spaces)
                                           |-> src/agent_api.py (Voice Agent API)
                                           |-> src/test_smoke.py (pytest 28)
```

- `src/main.py` — reusable core (portable to jobs/freelance, no contest-only code)
- `app.py` — demo entry (Gradio), wraps `build()`

## Results (replay with `python3 src/main.py "..."`)

- Before: booking via tiny-text apps (elderly give up) -> After: one spoken sentence + agent confirmation + booked slot
- Loop: book OK / barge-in (interruption → newer utterance wins) / escalation (unclear audio → human nurse)
- Real AssemblyAI numbers, English-only (`sample_en.wav`), re-verified 30/9 with live key:
  - Live realtime (`python3 src/realtime.py --src sample_en.wav`): handshake **~1.0s** + first PARTIAL **~1.2s** + FINAL **~3.9s** + Speaker A → `book a cardiology checkup tomorrow morning at nine`. Batch (`python3 src/main.py sample_en.wav`): backend `assemblyai-structured`, diarization Speaker A, listen_ms **~8.5s** (upload+poll, 8–25s queue-dependent).
  - Voice Agent API (`src/agent_api.py`, inline en session + English keyterms + barge-in + 2 tools): `python3 src/agent_api.py --print-session` (offline) + live `python3 src/agent_api.py --src sample_en.wav` (needs key, one-time token, direct voice WS, TTS, tool.call->tool.result local, session.end against billing hang). Remove AssemblyAI: no real hearing/TTS, only labeled local-sim typing — voice booking dies (load-bearing).
  - Realtime WS STT fallback (`src/realtime.py`, `u3-rt-pro + min_latency + language_codes=[en]` + English keyterms, auto-close 60s): handshake ~0.7-1.0s + PARTIAL ~1.1-1.3s + FINAL ~2.8-4.1s + Speaker A. Barge-in: interrupting FINAL → agent stops, uses newer utterance.
  - `understand` depends on **which provider actually answered**: local regex `<5ms`, Gemini ~0.4s, Nemotron ~7.5s (network + inference). The status bar and the `🔧 Technical` expander name the provider that really answered, including when it was a fallback — read that line rather than assuming. `act`/`speak` stay instant either way.
  - Hybrid: `structured_to_fields()` merges local + AssemblyAI into a live entity table, light TTS `src/tts.py` (edge-tts en fallback, missing lib → skip, never crash).
- pytest 28 passed (`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest src/ -q`)

## API keys needed (if any)

- `NEBIUS_API_KEY` (required for the real NLU — Nemotron via Nebius Token Factory; without it the app silently falls back to Gemini, then regex)
- `GEMINI_API_KEY` (fallback NLU when Nemotron times out)
- `ASSEMBLYAI_API_KEY` (optional, real STT for .wav/.mp3/.m4a) — free at https://www.assemblyai.com/ → API keys. Without a key it still runs labeled local-sim (backend labeled).
- Never commit real keys. Use environment variables (see `.gitignore`).

## Structure

- `src/main.py` — STT/batch fallback pipeline + tools (check/book, YES-gated strict)
- `src/agent_api.py` — managed Voice Agent API (one-time token + direct voice WS + TTS)
- `src/realtime.py` — streaming WS STT fallback (Universal-3-5-pro vi + diarization)
- `src/test_smoke.py` — smoke tests
- `app_streamlit.py` — main demo (single Streamlit URL for judges, 🎙 Voice Agent API demo button + labeled-backend fallback)
- `app.py` — secondary HF Spaces demo (Gradio), same `run_pipeline` wrapper (see file docstring)

## Credits & prior art (what we used vs what we built)

Workflow patterns studied on GitHub informed the design; all dialogue logic, English entity parsing, and the consent gate are original work:

- [ishanavasthi/clinicflow](https://github.com/ishanavasthi/clinicflow) — pattern: ask one thing at a time, never offer times before intake is complete, never claim a booking a tool didn't confirm.
- [tusharjain1003/VoiceIntake-AI](https://github.com/tusharjain1003/VoiceIntake-AI) — pattern: FSM voice loop + healthcare guardrails + eval harness; ours: 5-state FSM + 28 pytest scenarios.
- [abhishekpabbathi/clinic-voice-agent](https://github.com/abhishekpabbathi/clinic-voice-agent) — pattern: `CONFIRMED` booking records + per-stage latency logging.
- [JamesOkunlade/docbook-api](https://github.com/JamesOkunlade/docbook-api) / [KalebAsratemedhin/Efoy](https://github.com/KalebAsratemedhin/Efoy) — pattern: `specialty → doctor → schedule → appointment` with conflict rejection.

Built originally for this entry: EN specialty/doctor catalog + day/hour parsing, YES-gated booking (strict, AI understands ≠ AI books), ask-first slot-full handling, AssemblyAI Universal `en` keyterms + diarization wiring, full-English dialogue.

## Market (sourced TAM)

- Users: private clinics + over-60s who can't use tiny-text apps.
- Vietnam: ~12M over-60 (UNFPA 2023), ~5,000 private clinics (Ministry of Health est.).
- Starting SAM (team estimate): 500 clinics x $39/mo = $19,500 MRR = $234k ARR year 1.
- Revenue: SaaS $39/mo Solo / $99/mo Plus, cheaper than a ~$250/mo receptionist.
