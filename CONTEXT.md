# YouTube Downloader

A command-line tool for downloading, converting, and organizing media from YouTube videos, livestreams, and playlists.

## Language

**Target URL**:
The web address of a YouTube video, livestream, short, playlist, or channel to be retrieved.
_Avoid_: Link, web address, query

**Media Profile**:
A predefined configuration specifying video resolution, audio bitrate, codec, and container format.
_Avoid_: Quality preset, format string, download mode

**Download Task**:
A single discrete unit of work representing the retrieval, post-processing, and storage of media from a Target URL.
_Avoid_: Job, download item, download process

**Download Queue**:
An ordered collection of Download Tasks to be executed sequentially or concurrently.
_Avoid_: Batch list, task list

**Output Destination**:
The local directory structure where downloaded and converted media files are organized and saved.
_Avoid_: Save folder, download path, output folder

**Playlist Folder**:
A dedicated sub-directory created within the Output Destination to contain and index tracks from a playlist.
_Avoid_: Playlist dir, album folder

**Chapter Marker**:
Embedded metadata partitioning the media timeline into named sections.
_Avoid_: Timestamp, section split

**Subtitle Track**:
Embedded timed text stream providing captions or transcriptions.
_Avoid_: Captions file, SRT

**Livestream Recording**:
The continuous capture, remuxing, and finalization of an ongoing live broadcast from its beginning.
_Avoid_: Stream rip, live dump
