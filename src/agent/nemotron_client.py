#!/usr/bin/env python3
"""Nemotron NLU via Nebius Token Factory (OpenAI-compatible).

Drop-in alternative to the Gemini path in llm_client.py:
  nemotron_call(system, user, ...) -> str   (same contract as _gemini_call)

Key: NEBIUS_API_KEY (env / project .env — loaded by config._load_dotenv).
Model: NEMOTRON_MODEL env, default nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B.
Endpoint: NEBIUS_BASE_URL env, default https://api.tokenfactory.nebius.com/v1.

Raises RuntimeError on missing key or HTTP error so the existing
try/except fallbacks (regex-fallback) keep working unchanged.
"""
import json
import os
import urllib.request

from . import config  # noqa: F401  (side effect: loads project .env)

BASE_URL = (
    os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1").strip()
    or "https://api.tokenfactory.nebius.com/v1"
).rstrip("/")
MODEL = (
    os.getenv("NEMOTRON_MODEL", "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B").strip()
    or "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
)


def nemotron_call(system: str, user: str, timeout: float = 20.0,
                  temperature: float = 0.0, max_tokens: int = 512) -> str:
    key = (os.getenv("NEBIUS_API_KEY", "") or "").strip().strip("'").strip('"')
    if not key:
        raise RuntimeError("missing NEBIUS_API_KEY")
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user[:2000]},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key},
    )
    last = "{}"
    for _attempt in range(3):
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            out = json.loads(resp.read().decode("utf-8"))
        last = json.dumps(out)[:200]
        try:
            text = (out["choices"][0]["message"]["content"] or "").strip()
        except Exception:
            text = ""
        if text:
            return text
        # Nebius sometimes answers with an empty body. Retry rather than hand
        # an empty string to the caller, which reads as "fallback" downstream.
        time.sleep(0.8)
    raise RuntimeError("nemotron returned an empty body 3x: " + last)
