# 10 — Wizard Prompt Alignment & Model Property Integration

**What to build:** Align the interactive wizard in `wizard.py` to use `media_profile.supports_subtitles` consistently across all prompts and tests, ensuring audio-only profiles skip subtitle prompts cleanly in both interactive and automated execution paths.

**Blocked by:** 09 — Media Profile Format & Postprocessor Decoupling

**Status:** ready-for-agent

- [ ] Interactive wizard prompts query `media_profile.supports_subtitles` for subtitle configuration.
- [ ] Interactive wizard tests in `tests/test_wizard.py` verify prompt skips and option assignments for audio and video profiles.
