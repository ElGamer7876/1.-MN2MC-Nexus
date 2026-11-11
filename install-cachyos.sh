#!/usr/bin/env bash
set -Eeuo pipefail
cd -- "$(dirname -- "$0")"
if (( EUID == 0 )); then echo "Run as regular user, not root" >&2; exit 1; fi
for file in requirements.txt package-lock.json main.py; do
  if [[ ! -f "$file" ]]; then echo "Missing $file; run from the repository" >&2; exit 1; fi
done
if [[ "$#" -gt 0 && "$1" == "--dry-run" ]]; then
  echo "Would install Python 3.13, Node.js, dependencies, run Global wizard, optionally Paper 1.21.11."
  echo "No Global password login can be performed without a verified API."
  exit 0
fi
if ! command -v pacman >/dev/null; then echo "Requires CachyOS or Arch Linux" >&2; exit 1; fi
echo "MN2MC-Nexus CachyOS all-in-one installer"
echo "NOTICE: Real Global 1.7.15 account login and room hosting are still unsupported."
read -r -p "Install required system packages using pacman? [Y/n] " yn
if [[ ! "$yn" =~ ^[Nn]$ ]]; then
  sudo pacman -S --needed git uv nodejs npm jre21-openjdk curl jq
fi
for tool in uv npm node; do
  command -v "$tool" >/dev/null || { echo "Missing $tool" >&2; exit 1; }
done
uv python install 3.13
if [[ ! -x .venv/bin/python ]]; then uv venv --python 3.13 .venv; fi
uv pip install --python .venv/bin/python -r requirements.txt
npm ci
.venv/bin/python -m scripts.setup_global
read -r -p "Download stable Paper 1.21.11 for local testing? [y/N] " yn
if [[ "$yn" =~ ^[Yy]$ ]]; then .venv/bin/python -m scripts.install_paper; fi
echo "Done. Test: .venv/bin/python main.py --dry-run"
echo "Global: .venv/bin/python main.py --mode global"
echo "China: .venv/bin/python main.py --mode china"
echo "Both: .venv/bin/python main.py --mode both"
