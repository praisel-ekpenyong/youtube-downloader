# 14 — Deep Output Destination & Playlist Folder Management

**What to build:** Consolidate output destination resolution, directory verification, and playlist folder isolation into a cohesive destination management module. Callers provide target destinations without manual filesystem preparation or path template coordination.

**Blocked by:** 12 — Deep MediaDownloader & Option Translation Encapsulation

**Status:** resolved

- [x] Output destination verification and template formatting are encapsulated within a unified destination interface.
- [x] Playlist folder isolation and track naming rules are managed internally without leaking path formatting logic to callers.
- [x] CLI and engine interact with the destination module through a single resolution surface.
- [x] Automated tests verify directory creation, single video paths, and playlist track routing through the destination interface.

## Answer

Consolidated Output Destination resolution, directory creation, and playlist folder isolation into `OutputDestinationResolver` in `youtube_downloader.config`. The resolver presents a unified resolution surface supporting both `DownloadTask` instances and `MediaProfile` enums via `build_output_template` and `ensure_destination`. Single video/audio folder organization and playlist folder isolation (`Playlists/<Playlist Title>/<Index> - <Title> [<ID>].<ext>`) are managed entirely internally. `MediaDownloader` and the CLI interact with the destination resolver without leaking path formatting or filesystem preparation logic. All 82 unit and integration tests pass with 100% type safety.

