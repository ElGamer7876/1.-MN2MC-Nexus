#!/usr/bin/env python3
"""Install a stable Paper 1.21.11 build from the official PaperMC API."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

VERSION = "1.21.11"
API_URL = f"https://fill.papermc.io/v3/projects/paper/versions/{VERSION}/builds"
AGENT = "MN2MC-Nexus-Installer/0.1 (+https://github.com/ElGamer7876/1.-MN2MC-Nexus)"
DEST = Path("local-paper")

def fetch(url: str) -> bytes:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in ("fill.papermc.io", "fill-data.papermc.io"):
        raise ValueError("Untrusted Paper download URL")
    with urlopen(Request(url, headers={"User-Agent": AGENT}), timeout=60) as response:
        return response.read()

def select_build(items: list) -> tuple[str, str | None]:
    if not isinstance(items, list):
        raise ValueError("Invalid PaperMC builds response")
    stable = [item for item in items if item.get("channel") == "STABLE"]
    if not stable:
        raise RuntimeError("No stable Paper 1.21.11 build available")
    item = stable[0]["downloads"]["server:default"]
    return item["url"], item.get("checksums", {}).get("sha256")

def main() -> None:
    jar = DEST / "paper.jar"
    if jar.exists():
        print("Existing Paper JAR kept:", jar)
        return
    print("Fetching official PaperMC stable build...")
    url, sha256 = select_build(json.loads(fetch(API_URL)))
    payload = fetch(url)
    if not payload.startswith(b"PK\x03\x04"):
        raise RuntimeError("Not a valid JAR/ZIP download")
    if sha256 and hashlib.sha256(payload).hexdigest().lower() != sha256.lower():
        raise RuntimeError("Paper JAR checksum mismatch")
    DEST.mkdir(parents=True, exist_ok=True)
    temporary = DEST / "paper.jar.tmp"
    temporary.write_bytes(payload)
    os.replace(temporary, jar)
    (DEST / "server.properties").write_text(
        "server-ip=127.0.0.1\nserver-port=25565\nonline-mode=false\n"
        "max-players=40\nmotd=MN2MC-Nexus local only\n", encoding="utf-8"
    )
    (DEST / "README-FIRST.txt").write_text(
        "Read the Minecraft EULA and only if you accept it create eula.txt with eula=true.\n"
        "Launch: /usr/lib/jvm/java-21-openjdk/bin/java -Xms1G -Xmx3G -jar paper.jar --nogui\n"
        "IMPORTANT: online-mode=false only for LOCALHOST; never expose TCP 25565 publicly.\n"
        "Global Mini World crossplay is not yet verified or functional end-to-end.\n",
        encoding="utf-8",
    )
    print("Paper downloaded to", jar, "- read local-paper/README-FIRST.txt")

if __name__ == "__main__":
    main()
