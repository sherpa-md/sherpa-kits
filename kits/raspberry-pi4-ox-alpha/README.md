# Raspberry Pi 4 Ox Alpha Worker

This kit turns a 64-bit Raspberry Pi 4 into a lightweight OpenCode coding-agent machine using the cloud-hosted Ox Alpha preview model.

## Beginner path

Use the step-by-step [RaspberryPi4OxAlpha.sherpa.md](../../handoffs/RaspberryPi4OxAlpha.sherpa.md) guide.

## One-command installer

```bash
curl -fsSL https://raw.githubusercontent.com/sherpa-md/sherpa-kits/main/kits/raspberry-pi4-ox-alpha/install.sh | bash
```

## What the installer changes

- Installs required Debian packages.
- Installs OpenCode from its official installer when missing.
- Creates `~/.local/bin/pi-ox`.
- Sets `opencode/x-preview-f-free` as the default model.
- Creates an optional local-only user service file.
- Does not collect or include credentials.

## State

Draft and unverified on physical Raspberry Pi 4 hardware. The shell and JSON configuration have been statically checked. Hardware testing is still required.

