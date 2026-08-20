# 0004: PyWebView Desktop GUI Architecture

We decided to build the graphical user interface using `pywebview` with an HTML5, Tailwind CSS, and Vanilla JS frontend communicating directly with the Python backend via an in-process bridge.

While pure Python GUI toolkits (such as Tkinter or PyQt) avoid web technologies, they make modern, responsive styling and animations cumbersome. Conversely, Electron and Tauri introduce heavy Node.js or Rust build toolchains and substantial binary overhead. PyWebView leverages the operating system's native webview (Edge WebView2 on Windows) to deliver a lightweight desktop window with modern web styling, zero Node.js build dependencies, and zero open network ports.
