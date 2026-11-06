---
title: Downloads
description: Download the TLOW desktop app, browser app, CLI, or Python SDK
---

# Downloads

TLOW runs entirely on your hardware. Choose the interface that fits your workflow.

---

## Desktop App

The desktop app is a native window for the TLOW chat UI. All inference and backend
processing happens on your local machine — the app connects to the backend you start locally.

!!! info "Backend required"
    Start the backend before opening the desktop app. The quickstart script handles everything:
    ```bash
    git clone https://github.com/mrtate36/TLOW.git && cd TLOW
    ./scripts/quickstart.sh
    ```

### Download

| Platform | Download | Notes |
|----------|----------|-------|
| macOS (Apple Silicon) | [:material-download: **TLOW.dmg**](https://github.com/mrtate36/TLOW/releases/download/desktop-latest/TLOW_0.1.0_aarch64.dmg) | M1/M2/M3/M4 Macs |
| Windows (64-bit) | [:material-download: **TLOW-setup.exe**](https://github.com/mrtate36/TLOW/releases/download/desktop-latest/TLOW_0.1.0_x64-setup.exe) | Windows 10+ |
| Linux (DEB) | [:material-download: **TLOW.deb**](https://github.com/mrtate36/TLOW/releases/download/desktop-latest/TLOW_0.1.0_amd64.deb) | Ubuntu, Debian |
| Linux (RPM) | [:material-download: **TLOW.rpm**](https://github.com/mrtate36/TLOW/releases/download/desktop-latest/TLOW-0.1.0-1.x86_64.rpm) | Fedora, RHEL |
| Linux (AppImage) | [:material-download: **TLOW.AppImage**](https://github.com/mrtate36/TLOW/releases/download/desktop-latest/TLOW_0.1.0_amd64.AppImage) | Any distro |

!!! tip "All releases"
    Browse all versions on the [GitHub Releases](https://github.com/mrtate36/TLOW/releases) page.

### macOS: "app is damaged" fix

macOS Gatekeeper quarantines apps downloaded from the internet that aren't notarized
by Apple. If you see **"TLOW is damaged and can't be opened"**, run this in
Terminal to clear the quarantine flag:

```bash
xattr -cr /Applications/TLOW.app
```

Then open the app normally. If you installed from the DMG but haven't moved it to
`/Applications` yet, point the command at wherever the `.app` bundle is:

```bash
xattr -cr ~/Downloads/TLOW.app
```

!!! note
    This is standard for open-source macOS apps distributed outside the App Store.
    The command removes the quarantine extended attribute — it does not modify the app.

### What's included

The desktop app provides:

- **Full chat UI** — same interface as the browser app, in a native window
- **Energy monitoring** — real-time power consumption tracking
- **Telemetry dashboard** — token throughput, latency, and cost comparison vs. cloud models
- **System tray** — quick access without keeping a terminal open

The backend (Ollama, Python API server, inference) runs separately on your machine.

### Build from source

```bash
git clone https://github.com/mrtate36/TLOW.git
cd TLOW/desktop
npm install
npm run tauri build
```

The built installer will be in `frontend/src-tauri/target/release/bundle/`.

---

## Browser App

Run the full chat UI in your browser. Everything stays local — the backend runs on
your machine and the frontend connects via `localhost`.

### One-command setup

```bash
git clone https://github.com/mrtate36/TLOW.git
cd TLOW
./scripts/quickstart.sh
```

The script handles everything:

1. Checks for Python 3.10+ and Node.js 18+
2. Installs Ollama if not present and pulls a starter model
3. Installs Python and frontend dependencies
4. Starts the backend API server and frontend dev server
5. Opens `http://localhost:5173` in your browser

### Manual setup

If you prefer to run each step yourself:

=== "Step 1: Clone and install"

    ```bash
    git clone https://github.com/mrtate36/TLOW.git
    cd TLOW
    uv sync --extra server
    cd frontend && npm install && cd ..
    ```

=== "Step 2: Start Ollama"

    ```bash
    # Install from https://ollama.com if not already installed
    ollama serve &
    ollama pull qwen3:0.6b
    ```

=== "Step 3: Start backend"

    ```bash
    uv run tlow serve --port 8000
    ```

=== "Step 4: Start frontend"

    ```bash
    cd frontend
    npm run dev
    ```

Then open [http://localhost:5173](http://localhost:5173).

### What you get

- **Chat interface** — markdown rendering, streaming responses, conversation history
- **Tool use** — calculator, web search, code interpreter, file I/O
- **System panel** — live telemetry, energy monitoring, cost comparison vs. cloud models
- **Dashboard** — energy graphs, trace debugging, cost breakdown
- **Settings** — model selection, agent configuration, theme toggle

---

## CLI

The command-line interface is the fastest way to interact with TLOW
programmatically. Every feature is accessible from the terminal.

### Install

```bash
git clone https://github.com/mrtate36/TLOW.git
cd TLOW
uv sync
```

### Verify

```bash
tlow --version
# tlow, version 0.1.0
```

### First commands

```bash
# Ask a question
tlow ask "What is the capital of France?"

# Use an agent with tools
tlow ask --agent orchestrator --tools calculator "What is 137 * 42?"

# Start the API server
tlow serve --port 8000

# Run diagnostics
tlow doctor

# List available models
tlow model list

# Interactive chat
tlow chat
```

!!! info "Inference backend required"
    The CLI requires a running inference backend (e.g., Ollama). See the
    [Installation guide](getting-started/installation.md#setting-up-an-inference-backend)
    for setup instructions.

---

## Python SDK

For programmatic access, the `TLOW` class provides a high-level sync API.

### Install

```bash
git clone https://github.com/mrtate36/TLOW.git
cd TLOW
uv sync
```

### Quick example

```python
from tlow import TLOW

j = TLOW()
print(j.ask("Explain quicksort in two sentences."))
j.close()
```

### With agents and tools

```python
result = j.ask_full(
    "What is the square root of 144?",
    agent="orchestrator",
    tools=["calculator", "think"],
)
print(result["content"])       # "12"
print(result["tool_results"])  # tool invocations
print(result["turns"])         # number of agent turns
```

### Composition layer

For full control, use the `SystemBuilder`:

```python
from tlow import SystemBuilder

system = (
    SystemBuilder()
    .engine("ollama")
    .model("qwen3:8b")
    .agent("orchestrator")
    .tools(["calculator", "web_search", "file_read"])
    .enable_telemetry()
    .enable_traces()
    .build()
)

result = system.ask("Summarize the latest AI news.")
system.close()
```

See the [Python SDK guide](user-guide/python-sdk.md) for the full API reference.
