#!/usr/bin/env python3
"""Configure account UID and region; never request passwords without verified auth."""
import os
from pathlib import Path
import mn2mc.config as config

REGIONS = ("overseas", "usz", "hkz", "jpz")

def ask_uid(input_fn=input):
    while True:
        value = input_fn("Mini World Global UID: ").strip()
        if value.isdecimal() and 0 < int(value) < 2**63:
            return int(value)
        print("Invalid UID; please enter positive digits.")

def ask_region(input_fn=input):
    print("Regions: overseas / usz / hkz / jpz")
    print("These regions are candidates; account routing has not been officially verified.")
    while True:
        choice = input_fn("Account region [usz]: ").strip().lower() or "usz"
        if choice in REGIONS:
            return choice
        print("Choose overseas, usz, hkz or jpz.")

def ask_mode(input_fn=input):
    while True:
        choice = input_fn("Also enable China 1.58.0? [y/N] ").strip().lower()
        if choice in ("", "n", "no"):
            return "global"
        if choice in ("y", "yes"):
            return "both"
        print("Answer y or n.")

def main():
    if os.geteuid() == 0:
        raise SystemExit("Do not run as root")
    print("Mini World Global 1.7.15 setup")
    uid = ask_uid()
    region = ask_region()
    edition = ask_mode()
    config.load()
    config.nexus.region_mode = region
    config.nexus.region_accounts[region] = [str(uid)]
    config.nexus.runtime.mode = edition
    config.nexus.auto_expand_rooms = False
    config.mini.server.host_to_room_server = False
    config.save()
    Path("config.yaml").chmod(0o600)
    print("Local config.yaml saved with 0600 permissions.")
    print(f"UID {uid} in {region}. Edition: {edition}.")
    print("Global login is NOT IMPLEMENTED; no password was requested, stored or sent.")
    print("Use your OFFICIAL Mini World Global client to authenticate for now.")
    print("The prepared auth interface retries confirmed wrong passwords up to three times.")
    print("The local UDP listener cannot yet create or register Global rooms.")

if __name__ == "__main__":
    main()
