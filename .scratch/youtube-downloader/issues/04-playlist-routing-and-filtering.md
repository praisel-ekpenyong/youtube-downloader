# 04 — Playlist Routing & Index Filtering

**What to build:** Automatic detection of playlists, creating isolated subfolders `Downloads/YouTube/Playlists/<Playlist Title>/`, applying track numbering (`01 - Track.mp4`), and supporting item range selection (e.g. `--items 1-5`).

**Blocked by:** 02 — Core Downloader Engine & Video Media Profiles

**Status:** ready-for-agent

- [ ] Playlist detection creates dedicated subfolder named after the playlist title.
- [ ] Playlist items are sequenced with leading track numbers (e.g. `01 - Title.mp4`).
- [ ] CLI supports `--items` / `--playlist-items` range filtering (e.g. `1-5`, `10,12`).
- [ ] Unit tests verify playlist folder hierarchy and item selection flags.
