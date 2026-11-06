#!/usr/bin/env bash
# tlow-wrapper.sh — symlinked to ~/.local/bin/tlow.
# Activates the managed venv and execs the real tlow CLI.

TLOW_HOME="${TLOW_HOME:-$HOME/.tlow}"
VENV="$TLOW_HOME/.venv"

if [[ ! -d "$VENV" ]]; then
    echo "tlow: venv not found at $VENV" >&2
    echo "Re-run the installer: curl -fsSL https://mrtate36.github.io/TLOW/install.sh | bash" >&2
    exit 1
fi

exec "$VENV/bin/tlow" "$@"
