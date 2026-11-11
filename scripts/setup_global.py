#!/usr/bin/env python3
"""China-first interactive setup with explicit opt-in Global 1.7.15 BETA."""
import os
from pathlib import Path

import mn2mc.config as config
from mn2mc.nexus.regions import REGIONS

def ask_uid(input_fn=input):
    while True:
        value = input_fn("Mini World Global BETA UID: ").strip()
        if value.isdecimal() and 0 < int(value) < 2**63:
            return int(value)
        print("Invalid UID; enter positive digits.")

def ask_region(input_fn=input):
    print("Global BETA candidate regions: " + " / ".join(REGIONS))
    print("Hostnames come from archived client XML; login/region eligibility NOT verified.")
    while True:
        choice = input_fn("Your account's region code [usz]: ").strip().lower() or "usz"
        if choice in REGIONS:
            return choice
        print("Choose a listed region code, not a country name.")

def ask_mode(input_fn=input):
    while True:
        choice = input_fn("Enable experimental Mini World Global 1.7.15 BETA too? [y/N] ").strip().lower()
        if choice in ("", "no", "n"):
            return "china"
        if choice in ("yes", "y"):
            return "both"
        print("Answer y or n.")

def main():
    if os.geteuid() == 0:
        raise SystemExit("Do not run as root")
    print("=== MN2MC-Nexus: China 1.58.0 (main) + optional Global 1.7.15 BETA ===")
    mode = ask_mode()
    config.load()
    config.nexus.runtime.mode = mode
    config.nexus.runtime.global_beta_enabled = mode == "both"
    if mode == "both":
        uid = ask_uid()
        region = ask_region()
        config.nexus.region_mode = region
        config.nexus.region_accounts[region] = [str(uid)]
        config.nexus.auto_expand_rooms = False
        print("BETA UID and region stored locally as aliases, no authentication attempted.")
    else:
        print("China-only selected; no Global UID or password required.")
    config.save()
    Path("config.yaml").chmod(0o600)
    print("Settings saved to private config.yaml (0600).")
    print("China: UDP 11155 (default). Global BETA: UDP 11156 (optional).")
    print("Global password login, public room creation and playable crossplay are NOT validated.")
    print("No Global password was requested or transmitted.")

if __name__ == "__main__":
    main()
