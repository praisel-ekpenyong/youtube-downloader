# 01 — GUI App Shell & Bridge Foundation

**What to build:** A runnable desktop window launched via `ytdl-gui` that renders a modern dark-slate Tailwind interface inside `pywebview`. Establishes the in-process Python API bridge seam, verifies bidirectional communication between JavaScript and Python, and includes automated unit tests for bridge setup.

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

- [ ] Desktop window launches cleanly via `ytdl-gui` CLI command or python entry point.
- [ ] HTML5 and Tailwind CSS dark theme loads with YouTube-Studio-inspired slate background and header.
- [ ] In-process Python API bridge initializes and responds to basic status/ping requests from JavaScript.
- [ ] Unit tests verify bridge instantiation and JS-bridge communication contracts in headless test environments.
