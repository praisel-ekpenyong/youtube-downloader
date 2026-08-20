# 02 — Target URL Metadata Preview & Inspection

**What to build:** Asynchronous link inspection on the UI. When a user pastes or types a video or playlist URL, the frontend invokes the Python bridge to pre-fetch and display a live metadata preview card showing thumbnail artwork, title, duration, channel name, or playlist track count, with graceful error handling for invalid or unreachable links.

**Blocked by:** 01 — GUI App Shell & Bridge Foundation

**Status:** ready-for-agent

- [ ] Pasting a valid YouTube video URL asynchronously fetches and displays video title, thumbnail, channel name, and duration.
- [ ] Pasting a playlist URL identifies it as a playlist and displays the total item count.
- [ ] Loading states / skeleton placeholders are shown while metadata is being fetched.
- [ ] Invalid, private, or unreachable URLs display a clear warning badge without crashing the UI.
- [ ] Unit tests verify metadata extraction contracts and error handling at the bridge seam.
