# Docker Setup — Student Fitness App

This document explains how to build, test, and run the Android app using Docker, without needing Android Studio or a local Android SDK installation.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- **KVM** enabled on your host (required by the emulator service)

### Linux

```bash
# Verify KVM is available
sudo apt install cpu-checker
kvm-ok
```

### Windows 10 / 11 — Docker Desktop + WSL2 (no manual Linux VM needed)

Docker Desktop for Windows manages WSL2 automatically, so you do **not** need to set up a Linux VM by hand. Follow these steps once:

1. **Enable WSL2 and install Docker Desktop**
   - Open PowerShell as Administrator and run:
     ```powershell
     wsl --install
     ```
## Language name and summary
## EBNF (or link to GRAMMAR.md)
## Environment
## Run
## Test inputs (what each file covers)
## Output format (LABEL lexeme; EOF / NEWLINE / INDENT notes)
## AI / assistance
pose run --rm build sh -c "./gradlew connectedDebugAndroidTest --no-daemon"
  ```
