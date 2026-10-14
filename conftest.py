"""Pytest bootstrap — loaded before any test module imports the agent package.

Tests must be deterministic and offline. Without this file, a developer (or CI
image) with a populated .env silently exercises the live LLM path: the suite
was observed taking 6m06s with 3 failures, because the agent answered from
Nemotron instead of the labelled regex fallback the assertions expect.

Neutralising the keys here wins over config._load_dotenv(), which only sets a
variable when it is absent from os.environ (config.py: `k not in os.environ`).
Streamlit secrets and real deployments are unaffected — this runs under pytest
only.
"""

import os

# Keys the agent reads. Empty string -> has_nebius()/has_gemini()/has_assemblyai()
# all report False, so _has_any_llm_key() is False and calls stay local.
for _key in ("NEBIUS_API_KEY", "GEMINI_API_KEY", "ASSEMBLYAI_API_KEY"):
    os.environ[_key] = ""

# Deterministic clock/seed-independent behaviour also depends on the demo slot
# store being empty; tests reset it themselves where they care.