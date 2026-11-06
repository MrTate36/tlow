#!/usr/bin/env bash
# tlow-uninstall.sh — clean removal of TLOW from $HOME.
#
# Removes:
#   ~/.tlow/
#   ~/.local/bin/tlow
#   ~/.local/bin/tlow-uninstall
#
# Does NOT remove: ollama, uv, or the Rust toolchain.

set -euo pipefail

TLOW_HOME="${TLOW_HOME:-$HOME/.tlow}"

if [[ -f "$TLOW_HOME/.state/bg.pid" ]]; then
    pid=$(cat "$TLOW_HOME/.state/bg.pid" 2>/dev/null || echo "")
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
        echo "Stopping background work (pid=$pid)..."
        kill "$pid" 2>/dev/null || true
    fi
fi

if command -v ollama >/dev/null 2>&1; then
    ollama stop >/dev/null 2>&1 || true
fi

if [[ -d "$TLOW_HOME" ]]; then
    rm -rf "$TLOW_HOME"
    echo "Removed $TLOW_HOME"
fi

for f in "$HOME/.local/bin/tlow" "$HOME/.local/bin/tlow-uninstall"; do
    if [[ -L "$f" ]] || [[ -f "$f" ]]; then
        rm -f "$f"
        echo "Removed $f"
    fi
done

cat <<EOF

TLOW removed.

Left intact (may be used by other tools):
  - Ollama       (uninstall: brew uninstall ollama  /  rm -f /usr/local/bin/ollama)
  - uv           (uninstall: rm -rf ~/.local/share/uv ~/.cargo/bin/uv)
  - Rust toolchain (uninstall: rustup self uninstall)
EOF
