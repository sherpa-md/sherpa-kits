# Raspberry Pi 4 + Ox Alpha

> **State:** Draft and unverified on physical Raspberry Pi 4 hardware. Ox Alpha is a limited-time preview model.

This installs OpenCode on a 64-bit Raspberry Pi 4 and sets its default model to OpenCode Zen's free Ox Alpha model. The Pi supplies the files and tools; the AI model runs in the cloud.

## What you need

- Raspberry Pi 4 with a 64-bit Raspberry Pi OS
- 4 GB RAM minimum; 8 GB is better
- Internet connection
- Keyboard/monitor or SSH terminal access
- An OpenCode Zen account and API key

## Easy installation

Open Terminal on the Raspberry Pi. Copy and paste this entire line, then press Enter:

```bash
curl -fsSL https://raw.githubusercontent.com/sherpa-md/sherpa-kits/main/kits/raspberry-pi4-ox-alpha/install.sh | bash
```

When it finishes, close Terminal and open it again. Then connect the model account:

```bash
opencode auth login
```

Choose **OpenCode Zen** and enter your own API key when asked. Do not send the key to anyone or post it online.

## Test it

```bash
pi-ox run "Say: Ox Alpha is working on my Raspberry Pi."
```

## Use it in a project

Move into the project folder and start the agent:

```bash
cd ~/my-project
pi-ox
```

If `~/my-project` does not exist yet:

```bash
mkdir -p ~/my-project
cd ~/my-project
pi-ox
```

## Important

- Ox Alpha does not run inside the Pi. The Pi must remain online.
- Ox Alpha is currently free but OpenCode describes it as limited-time.
- Its underlying model maker is not publicly disclosed.
- Review changes before committing or uploading them.
- This does not connect to anybody else's private Hermes system.

## Help

Check the installation:

```bash
pi-ox doctor
```

Supporting files: [raspberry-pi4-ox-alpha kit](../kits/raspberry-pi4-ox-alpha/)

