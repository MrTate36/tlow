# systemd Service (Linux)

TLOW includes a systemd unit file for running the API server as a managed background service on Linux. This provides automatic startup on boot, crash recovery, and integration with standard Linux service management tools.

## Prerequisites

Before installing the service, ensure that:

1. TLOW is installed in a virtual environment at `/opt/tlow/.venv` (or adjust paths accordingly).
2. A dedicated `tlow` system user exists (recommended for security).
3. An inference engine (such as Ollama) is running and accessible.

Create the user and installation directory:

```bash
sudo useradd --system --create-home --home-dir /opt/tlow tlow
sudo -u tlow python3 -m venv /opt/tlow/.venv
sudo -u tlow git clone https://github.com/mrtate36/TLOW.git /opt/tlow/TLOW
cd /opt/tlow/TLOW && sudo -u tlow uv sync --extra server
```

## Installing the Service

Copy the unit file to the systemd directory, reload the daemon, and enable the service:

```bash
sudo cp deploy/systemd/tlow.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tlow
sudo systemctl start tlow
```

Verify it is running:

```bash
sudo systemctl status tlow
```

## Service File Reference

The provided unit file at `deploy/systemd/tlow.service`:

```ini
[Unit]
Description=TLOW API Server
After=network.target

[Service]
Type=simple
User=tlow
WorkingDirectory=/opt/tlow
ExecStart=/opt/tlow/.venv/bin/tlow serve --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=5
Environment=HOME=/opt/tlow

[Install]
WantedBy=multi-user.target
```

### `[Unit]` Section

| Directive     | Value              | Description                                                                 |
|---------------|--------------------|-----------------------------------------------------------------------------|
| `Description` | `TLOW API Server` | Human-readable name shown in `systemctl status` and logs.              |
| `After`       | `network.target`   | Delays startup until the network stack is available, since the server binds to a network socket and may need to reach a remote engine. |

### `[Service]` Section

| Directive          | Value                                                              | Description                                                                                     |
|--------------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `Type`             | `simple`                                                           | The process started by `ExecStart` is the main service process. systemd considers the service started immediately. |
| `User`             | `tlow`                                                       | Runs the server as the `tlow` user rather than root, limiting the blast radius of any security issue. |
| `WorkingDirectory` | `/opt/tlow`                                                  | Sets the working directory for the process. This is where TLOW looks for local files and writes data. |
| `ExecStart`        | `/opt/tlow/.venv/bin/tlow serve --host 0.0.0.0 --port 8000` | The command to start the server. Uses the full path to the `tlow` binary inside the virtual environment. |
| `Restart`          | `on-failure`                                                       | Automatically restarts the service if it exits with a non-zero exit code. Does not restart on clean shutdown (`systemctl stop`). |
| `RestartSec`       | `5`                                                                | Waits 5 seconds before attempting a restart, preventing rapid restart loops if the service crashes immediately on startup. |
| `Environment`      | `HOME=/opt/tlow`                                             | Sets the `HOME` environment variable so TLOW finds its configuration at `~/.tlow/config.toml` (resolving to `/opt/tlow/.tlow/config.toml`). |

### `[Install]` Section

| Directive    | Value               | Description                                                                                 |
|--------------|---------------------|---------------------------------------------------------------------------------------------|
| `WantedBy`   | `multi-user.target` | The service starts when the system reaches multi-user mode (standard boot target for servers). `systemctl enable` creates a symlink under this target. |

## Configuration Options

### Changing the Bind Address and Port

Edit the `ExecStart` line to change the host or port:

```ini
ExecStart=/opt/tlow/.venv/bin/tlow serve --host 127.0.0.1 --port 9000
```

!!! tip
    Binding to `127.0.0.1` restricts access to localhost only. Use this when running behind a reverse proxy like Nginx or Caddy.

### Setting the Engine and Model

Pass additional flags to `tlow serve`:

```ini
ExecStart=/opt/tlow/.venv/bin/tlow serve --host 0.0.0.0 --port 8000 --engine ollama --model qwen3:8b
```

### Adding Environment Variables

Add multiple `Environment` directives or use `EnvironmentFile` for complex configurations:

```ini
[Service]
Environment=HOME=/opt/tlow
Environment=TLOW_ENGINE_DEFAULT=vllm
Environment=TLOW_OLLAMA_HOST=http://localhost:11434
```

Or load from a file:

```ini
[Service]
EnvironmentFile=/opt/tlow/.env
```

### Changing the User

If you prefer a different service user, update both the `User` directive and the paths:

```ini
[Service]
User=myuser
WorkingDirectory=/home/myuser/tlow
ExecStart=/home/myuser/tlow/.venv/bin/tlow serve --host 0.0.0.0 --port 8000
Environment=HOME=/home/myuser/tlow
```

### Using a Configuration File

Ensure the configuration file exists at the path where `HOME` points:

```bash
sudo -u tlow mkdir -p /opt/tlow/.tlow
sudo -u tlow cp config.toml /opt/tlow/.tlow/config.toml
```

The server reads `~/.tlow/config.toml` on startup, where `~` resolves from the `HOME` environment variable.

## Viewing Logs

TLOW logs are captured by journald. View them with `journalctl`:

```bash
# View all logs for the service
sudo journalctl -u tlow

# Follow logs in real time
sudo journalctl -u tlow -f

# View logs since the last boot
sudo journalctl -u tlow -b

# View logs from the last hour
sudo journalctl -u tlow --since "1 hour ago"

# View only error-level messages
sudo journalctl -u tlow -p err
```

## Managing the Service

### Start, Stop, and Restart

```bash
# Start the service
sudo systemctl start tlow

# Stop the service
sudo systemctl stop tlow

# Restart the service (stop + start)
sudo systemctl restart tlow

# Reload configuration without full restart (sends SIGHUP)
sudo systemctl reload-or-restart tlow
```

### Check Status

```bash
sudo systemctl status tlow
```

Example output:

```
● tlow.service - TLOW API Server
     Loaded: loaded (/etc/systemd/system/tlow.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-02-21 10:00:00 UTC; 2h ago
   Main PID: 12345 (tlow)
      Tasks: 4 (limit: 4915)
     Memory: 256.0M
        CPU: 1min 23s
     CGroup: /system.slice/tlow.service
             └─12345 /opt/tlow/.venv/bin/python /opt/tlow/.venv/bin/tlow serve --host 0.0.0.0 --port 8000
```

### Enable and Disable on Boot

```bash
# Enable automatic start on boot
sudo systemctl enable tlow

# Disable automatic start on boot
sudo systemctl disable tlow
```

### Apply Changes After Editing the Unit File

After modifying `/etc/systemd/system/tlow.service`, reload the systemd daemon and restart the service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart tlow
```

## Running Alongside Ollama

If Ollama is also managed via systemd, you can add an ordering dependency so the TLOW service waits for Ollama to start:

```ini
[Unit]
Description=TLOW API Server
After=network.target ollama.service
Requires=ollama.service
```

| Directive  | Description                                                              |
|------------|--------------------------------------------------------------------------|
| `After`    | Ensures TLOW starts after Ollama.                                  |
| `Requires` | If Ollama fails to start, TLOW will not start either.              |

!!! note
    Use `Wants` instead of `Requires` if you want TLOW to start even when Ollama is unavailable (for example, if you plan to start Ollama manually later).
