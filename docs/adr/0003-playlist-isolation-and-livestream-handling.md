# 0003: Playlist Isolation and Livestream Handling

We decided to automatically isolate playlist downloads into dedicated subdirectories and enforce resilient livestream capture.

Playlists will automatically save into `<Output Destination>/Playlists/<Playlist Title>/` with sequential numbering (`01 - Title.mp4`) and optional index filtering. Livestreams will capture from start (`--live-from-start`) and handle process interrupts cleanly, ensuring recorded fragments are remuxed into a valid, playable media container upon termination.
