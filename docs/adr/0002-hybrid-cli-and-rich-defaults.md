# 0002: Hybrid CLI and Rich Defaults

We decided to implement a hybrid CLI interaction model and rich default media enrichment.

When executed with arguments, the CLI runs headlessly for scripting and automation; when executed bare without arguments, it launches an interactive Rich wizard prompting the user for input and Media Profile. Furthermore, downloads will embed metadata, thumbnail artwork, chapter markers, and available subtitles by default (with explicit opt-out flags), ensuring saved media is organized and self-contained.
