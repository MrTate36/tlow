# CLI Reference

TLOW provides a command-line interface through the `tlow` command. Built on [Click](https://click.palletsprojects.com/), it offers subcommands for querying models, managing memory, running benchmarks, and serving an OpenAI-compatible API.

## Global Options

```bash
tlow --version   # Print the TLOW version
tlow --help      # Show top-level help with all subcommands
```

## `tlow init`

Detect local hardware (CPU, GPU, RAM) and generate a configuration file at `~/.tlow/config.toml`.

```bash
tlow init           # Interactive — refuses to overwrite existing config
tlow init --force   # Overwrite existing config without prompting
```

| Option    | Description                                   |
|-----------|-----------------------------------------------|
| `--force` | Overwrite existing configuration without prompting |

The `init` command auto-detects:

- **Platform** (Linux, macOS, Windows)
- **CPU** brand and core count
- **RAM** in GB
- **GPU** vendor, model, VRAM, and count (via `nvidia-smi`, `rocm-smi`, or `system_profiler`)

Based on the detected hardware, it recommends an appropriate inference engine and writes a pre-configured TOML file.

**Example output:**

```
Detecting hardware...
  Platform : linux
  CPU      : AMD Ryzen 9 7950X (32 cores)
  RAM      : 64 GB
  GPU      : NVIDIA RTX 4090 (24.0 GB VRAM, x1)

Config written successfully.
```

---

## `tlow ask`

Send a query to the inference engine (directly or through an agent) and print the response.

```bash
tlow ask "What is the capital of France?"
```

### Options

| Option                        | Type    | Default    | Description                                           |
|-------------------------------|---------|------------|-------------------------------------------------------|
| `-m`, `--model MODEL`         | string  | auto       | Model to use for inference                             |
| `-e`, `--engine ENGINE`       | string  | auto       | Engine backend (ollama, vllm, llamacpp, etc.)          |
| `-t`, `--temperature TEMP`    | float   | `0.7`      | Sampling temperature                                   |
| `--max-tokens N`              | int     | `1024`     | Maximum tokens to generate                             |
| `--json`                      | flag    | off        | Output raw JSON result instead of plain text           |
| `--no-stream`                 | flag    | off        | Disable streaming (synchronous mode)                   |
| `--no-context`                | flag    | off        | Disable memory context injection                       |
| `-a`, `--agent AGENT`         | string  | none       | Agent to use (`simple`, `orchestrator`)                |
| `--tools TOOLS`               | string  | none       | Comma-separated tool names to enable                   |

### Direct Mode vs Agent Mode

**Direct mode** (default) sends the query straight to the inference engine:

```bash
tlow ask "Explain quantum computing"
```

**Agent mode** routes the query through an agent that can use tools and manage multi-turn interactions:

```bash
tlow ask --agent orchestrator "What is 2+2?"
tlow ask --agent orchestrator --tools calculator,think "Calculate sqrt(144) + 3^2"
tlow ask --agent simple "Hello"
```

### Usage Examples

```bash
# Basic query
tlow ask "What is machine learning?"

# Specify a model
tlow ask -m qwen3:8b "Summarize this concept"

# Use the orchestrator agent with tools
tlow ask --agent orchestrator --tools calculator "What is 15% of 340?"

# Get JSON output
tlow ask --json "Hello"

# Disable memory context injection
tlow ask --no-context "Tell me about Python"

# Set maximum token generation
tlow ask --max-tokens 2048 "Write a detailed essay about AI"
```

### JSON Output Format

When using `--json` in **direct mode**, the output includes:

```json
{
  "content": "The response text...",
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 85,
    "total_tokens": 97
  }
}
```

When using `--json` in **agent mode**, the output includes:

```json
{
  "content": "The response text...",
  "turns": 3,
  "tool_results": [
    {
      "tool_name": "calculator",
      "content": "51.0",
      "success": true
    }
  ]
}
```

---

## `tlow model`

Manage and inspect language models available on running engines.

### `tlow model list`

List all models available from running inference engines, displayed as a Rich table with model parameters, context length, and VRAM requirements.

```bash
tlow model list
```

**Example output:**

```
           Available Models
┌─────────┬────────────────┬────────┬─────────┬──────┐
│ Engine  │ Model          │ Params │ Context │ VRAM │
├─────────┼────────────────┼────────┼─────────┼──────┤
│ ollama  │ qwen3:8b       │ 8B     │ 32,768  │ 6GB  │
│ ollama  │ llama3.2:3b    │ 3B     │ 8,192   │ 3GB  │
└─────────┴────────────────┴────────┴─────────┴──────┘
```

### `tlow model info <model>`

Show detailed information about a specific model.

```bash
tlow model info qwen3:8b
```

**Example output:**

```
┌─ Qwen 3 8B ──────────────────────────────┐
│ Model ID:     qwen3:8b                    │
│ Name:         Qwen 3 8B                   │
│ Parameters:   8B                          │
│ Context:      32,768                      │
│ Quantization: none                        │
│ Min VRAM:     6GB                         │
│ Engines:      ollama, vllm                │
│ Provider:     Alibaba                     │
│ API Key:      not required                │
└───────────────────────────────────────────┘
```

### `tlow model pull <model>`

Download a model via Ollama. Shows a progress bar during download.

```bash
tlow model pull qwen3:8b
```

!!! note
    The `pull` command requires a running Ollama instance. It connects to the Ollama API at the host configured in your `config.toml`.

---

## `tlow pearl`

Access Pearl's native node, wallet, and RPC tools from the TLOW CLI.

```bash
tlow pearl doctor
tlow pearl node -- <pearld args>
tlow pearl wallet -- <oyster args>
tlow pearl ctl -- <prlctl args>
tlow pearl address
```

All Pearl wrapper commands use the `tlow pearl <command>` shape. The
pass-through commands map to Pearl's native binaries:

| TLOW command | Pearl binary | Use |
|--------------------|--------------|-----|
| `tlow pearl doctor` | n/a | Check whether `pearld`, `oyster`, and `prlctl` are discoverable |
| `tlow pearl node` | `pearld` | Run the Pearl full node |
| `tlow pearl wallet` | `oyster` | Run the Oyster wallet daemon |
| `tlow pearl ctl` | `prlctl` | Query Pearl node or wallet RPC |
| `tlow pearl address` | `prlctl --wallet getnewaddress` | Generate a wallet address from Oyster |

Use `PEARL_HOME=/path/to/pearl` or `--pearl-home /path/to/pearl` if Pearl's
`bin/` directory is not on `PATH`. See the [Pearl CLI guide](pearl.md) for
examples.

---

## `tlow memory`

Manage the document memory store for retrieval-augmented generation.

### `tlow memory index <path>`

Index documents from a file or directory into the memory store.

```bash
tlow memory index ./docs/
tlow memory index ./notes.md
tlow memory index ./data/ --chunk-size 256 --chunk-overlap 32
tlow memory index ./docs/ --backend sqlite
```

| Option                      | Type   | Default | Description                          |
|-----------------------------|--------|---------|--------------------------------------|
| `--backend`, `-b`           | string | config  | Override the default memory backend  |
| `--chunk-size`              | int    | `512`   | Chunk size in tokens                 |
| `--chunk-overlap`           | int    | `64`    | Overlap between chunks in tokens     |

The ingestion pipeline supports text, markdown, code files, and PDF (with `pdfplumber` installed). Binary files and hidden directories are automatically skipped.

### `tlow memory search <query>`

Search the memory store for relevant document chunks.

```bash
tlow memory search "machine learning basics"
tlow memory search -k 10 "neural networks"
tlow memory search --backend faiss "embeddings"
```

| Option             | Type   | Default | Description                          |
|--------------------|--------|---------|--------------------------------------|
| `--top-k`, `-k`    | int    | `5`     | Number of results to return          |
| `--backend`, `-b`  | string | config  | Override the default memory backend  |

Results are displayed in a table with rank, score, source file, and a content preview.

### `tlow memory stats`

Show memory store statistics including document count and database size.

```bash
tlow memory stats
tlow memory stats --backend sqlite
```

| Option             | Type   | Default | Description                          |
|--------------------|--------|---------|--------------------------------------|
| `--backend`, `-b`  | string | config  | Override the default memory backend  |

---

## `tlow telemetry`

Query and manage inference telemetry data stored in SQLite.

### `tlow telemetry stats`

Show aggregated telemetry statistics including total calls, tokens, cost, and latency, broken down by model and engine.

```bash
tlow telemetry stats
tlow telemetry stats -n 5    # Show top 5 models
```

| Option          | Type | Default | Description                   |
|-----------------|------|---------|-------------------------------|
| `-n`, `--top`   | int  | `10`    | Number of top models to show  |

### `tlow telemetry export`

Export raw telemetry records in JSON or CSV format.

```bash
tlow telemetry export                          # JSON to stdout
tlow telemetry export --format csv             # CSV to stdout
tlow telemetry export --format json -o data.json  # JSON to file
tlow telemetry export -f csv -o metrics.csv    # CSV to file
```

| Option                | Type   | Default  | Description                     |
|-----------------------|--------|----------|---------------------------------|
| `-f`, `--format`      | choice | `json`   | Output format: `json` or `csv`  |
| `-o`, `--output`      | path   | stdout   | Output file path                |

### `tlow telemetry clear`

Delete all telemetry records from the database.

```bash
tlow telemetry clear         # Interactive confirmation
tlow telemetry clear --yes   # Skip confirmation
```

| Option         | Type | Default | Description                   |
|----------------|------|---------|-------------------------------|
| `-y`, `--yes`  | flag | off     | Skip confirmation prompt      |

!!! warning
    This permanently deletes all stored telemetry data. Use `--yes` to skip the confirmation prompt in automated scripts.

---

## `tlow bench`

Run inference benchmarks against a running engine.

### `tlow bench run`

Execute benchmarks and report results.

```bash
tlow bench run                               # Run all benchmarks, 10 samples
tlow bench run -n 20                         # 20 samples per benchmark
tlow bench run -b latency                    # Only the latency benchmark
tlow bench run -b throughput -n 50 --json    # Throughput, 50 samples, JSON output
tlow bench run -o results.jsonl              # Write JSONL results to file
tlow bench run -m qwen3:8b -e ollama         # Specific model and engine
```

| Option                     | Type   | Default | Description                              |
|----------------------------|--------|---------|------------------------------------------|
| `-m`, `--model MODEL`      | string | auto    | Model to benchmark                       |
| `-e`, `--engine ENGINE`    | string | auto    | Engine backend                           |
| `-n`, `--samples N`        | int    | `10`    | Number of samples per benchmark          |
| `-b`, `--benchmark NAME`   | string | all     | Specific benchmark to run                |
| `-o`, `--output PATH`      | path   | none    | Write JSONL results to file              |
| `--json`                   | flag   | off     | Output JSON summary to stdout            |

Available benchmarks:

- **latency** -- Measures per-call inference latency (mean, p50, p95, min, max)
- **throughput** -- Measures tokens-per-second throughput

---

## `tlow channel`

Manage messaging channels for multi-platform communication. Channels connect directly to platform APIs (Telegram, Discord, Slack, etc.) -- no gateway required.

### `tlow channel list`

List registered channel backends and their connection status.

```bash
tlow channel list
```

### `tlow channel send`

Send a message to a specific channel.

```bash
tlow channel send slack "Hello from TLOW!"
tlow channel send discord "Build complete"
```

| Argument    | Type   | Description                          |
|-------------|--------|--------------------------------------|
| `TARGET`    | string | Channel name to send to              |
| `MESSAGE`   | string | Message content                      |

### `tlow channel status`

Show connection status for configured channels.

```bash
tlow channel status
```

!!! note "Channel Dependencies"
    Each channel requires its platform-specific credentials (bot tokens, API keys) configured in the `[channel.<platform>]` section of your config. See [Configuration](../getting-started/configuration.md) for details.

---

## `tlow serve`

Start an OpenAI-compatible API server.

```bash
tlow serve                                 # Default host/port from config
tlow serve --port 8000                     # Custom port
tlow serve --host 0.0.0.0 --port 9000      # Bind to all interfaces
tlow serve --model qwen3:8b                # Specify default model
tlow serve --agent orchestrator            # Route requests through an agent
```

| Option                   | Type   | Default | Description                              |
|--------------------------|--------|---------|------------------------------------------|
| `--host HOST`            | string | config  | Bind address                             |
| `--port PORT`            | int    | config  | Port number                              |
| `-e`, `--engine ENGINE`  | string | auto    | Engine backend                           |
| `-m`, `--model MODEL`    | string | config  | Default model for inference              |
| `-a`, `--agent AGENT`    | string | none    | Agent for non-streaming requests         |

!!! note "Server Dependencies"
    The `serve` command requires the server extra:

    ```bash
    uv sync --extra server
    ```

    This installs FastAPI, uvicorn, and related dependencies.

### API Endpoints

The server exposes the following OpenAI-compatible endpoints:

| Method | Path                     | Description                    |
|--------|--------------------------|--------------------------------|
| POST   | `/v1/chat/completions`   | Chat completions (streaming & non-streaming) |
| GET    | `/v1/models`             | List available models          |
| GET    | `/health`                | Health check                   |
| GET    | `/v1/channels`           | List available messaging channels    |
| POST   | `/v1/channels/send`      | Send a message to a channel          |
| GET    | `/v1/channels/status`    | Channel bridge connection status     |

**Example with curl:**

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:8b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

When an agent is configured (e.g., `--agent orchestrator`), non-streaming requests are routed through the agent with access to all registered tools. For tool-capable agents (`orchestrator`, `react`, `openhands`), all registered tools are automatically loaded and made available.

---

## LLM-guided spec search (no CLI yet)

LLM-guided spec search (the frontier-driven harness-learning subsystem)
is exposed as a Python library only — there is currently no top-level
`tlow` subcommand for it. Construct a `SpecSearchOrchestrator`
directly from `tlow.learning.spec_search.orchestrator` and call
`.run(trigger)` with a trigger from
`tlow.learning.spec_search.triggers`. See
[`docs/user-guide/llm-guided-spec-search.md`](llm-guided-spec-search.md)
for the architecture and the building blocks
(`splits.py`, external corpora, `external_adapter`).
