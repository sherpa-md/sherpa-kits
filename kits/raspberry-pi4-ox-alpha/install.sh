#!/usr/bin/env bash
set -euo pipefail

MODEL="opencode/x-preview-f-free"

case "$(uname -m)" in
  aarch64|arm64) ;;
  *) echo "STOP: This needs a Raspberry Pi running a 64-bit ARM operating system." >&2; exit 1 ;;
esac

if [ "$(getconf LONG_BIT)" != "64" ]; then
  echo "STOP: Install the 64-bit version of Raspberry Pi OS first." >&2
  exit 1
fi

echo "Installing Raspberry Pi 4 + OpenCode + Ox Alpha..."
sudo apt-get update
sudo apt-get install -y curl git ca-certificates jq ripgrep

if ! command -v opencode >/dev/null 2>&1 && [ ! -x "$HOME/.opencode/bin/opencode" ]; then
  curl -fsSL https://opencode.ai/install | bash
fi

if command -v opencode >/dev/null 2>&1; then
  OPENCODE_BIN="$(command -v opencode)"
elif [ -x "$HOME/.opencode/bin/opencode" ]; then
  OPENCODE_BIN="$HOME/.opencode/bin/opencode"
else
  echo "STOP: OpenCode was downloaded, but its program could not be found." >&2
  exit 1
fi

mkdir -p "$HOME/.local/bin" "$HOME/.config/opencode" "$HOME/.config/systemd/user" "$HOME/pi-ox-workspace"

cat > "$HOME/.local/bin/pi-ox" <<WRAPPER
#!/usr/bin/env bash
set -euo pipefail
OPENCODE_BIN="$OPENCODE_BIN"
MODEL="$MODEL"
if [ "\${1:-}" = "doctor" ]; then
  echo "OpenCode: \$OPENCODE_BIN"
  "\$OPENCODE_BIN" --version
  echo "Model: \$MODEL"
  "\$OPENCODE_BIN" models opencode | grep -F x-preview-f-free
  exit 0
fi
if [ "\${1:-}" = "run" ]; then
  shift
  exec "\$OPENCODE_BIN" run --model "\$MODEL" "\$@"
fi
exec "\$OPENCODE_BIN" --model "\$MODEL" "\$@"
WRAPPER
chmod 0755 "$HOME/.local/bin/pi-ox"

CONFIG="$HOME/.config/opencode/opencode.json"
if [ -f "$CONFIG" ]; then
  cp "$CONFIG" "$CONFIG.before-pi-ox"
fi
cat > "$CONFIG" <<JSON
{
  "\$schema": "https://opencode.ai/config.json",
  "model": "$MODEL",
  "share": "disabled"
}
JSON

cat > "$HOME/.config/systemd/user/pi-ox-alpha.service" <<SERVICE
[Unit]
Description=Pi OpenCode Ox Alpha worker
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$HOME/pi-ox-workspace
ExecStart=$OPENCODE_BIN serve --hostname 127.0.0.1 --port 4096
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
SERVICE
systemctl --user daemon-reload

echo
echo "INSTALLATION COMPLETE"
echo "1. Close this Terminal and open it again."
echo "2. Run: opencode auth login"
echo "3. Choose OpenCode Zen and enter your own key."
echo "4. Test it with: pi-ox run \"Say: Ox Alpha is working.\""
