# 06 — Custom Profile CLI Support & Terminology Alignment

**What to build:** Add `--custom-format` / `-f` CLI option so `--profile custom` allows passing a custom format string. Standardize the output directory CLI option to `--output-destination` (with `--output-dir` and `-o` aliases) to align with domain vocabulary in `CONTEXT.md`. Remove the unrequested `--dry-run` flag from the CLI.

**Blocked by:** None — can start immediately.

**Status: resolved**

- [x] CLI accepts `--custom-format` / `-f` and passes it to `DownloadTask.custom_format` when using custom profile.
- [x] CLI supports `--output-destination` (with `--output-dir` and `-o` aliases) matching domain glossary.
- [x] Unrequested `--dry-run` flag is removed from CLI interface.
- [x] Unit tests in `tests/test_cli.py` verify `--custom-format`, `--output-destination`, and custom profile behavior.
