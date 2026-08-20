# 14 — Deep Output Destination & Playlist Folder Management

**What to build:** Consolidate output destination resolution, directory verification, and playlist folder isolation into a cohesive destination management module. Callers provide target destinations without manual filesystem preparation or path template coordination.

**Blocked by:** 12 — Deep MediaDownloader & Option Translation Encapsulation

**Status:** ready-for-agent

- [ ] Output destination verification and template formatting are encapsulated within a unified destination interface.
- [ ] Playlist folder isolation and track naming rules are managed internally without leaking path formatting logic to callers.
- [ ] CLI and engine interact with the destination module through a single resolution surface.
- [ ] Automated tests verify directory creation, single video paths, and playlist track routing through the destination interface.
