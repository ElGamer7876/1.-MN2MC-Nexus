#!/usr/bin/env python3
"""Compare your LOCAL unmodified Global client XML with catalog assumptions.

Offline-only. No network, authentication, game patching, or credential use.
No extracted client assets are copied into the repository.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from mn2mc.nexus.regions import REGIONS

MAX_XML_BYTES = 256 * 1024

def inspect_xml(filename: Path) -> dict:
    if not filename.is_file():
        raise FileNotFoundError(str(filename))
    if filename.stat().st_size > MAX_XML_BYTES:
        raise ValueError("Client XML exceeds inspection size limit")
    root = ElementTree.fromstring(filename.read_bytes())
    if root.tag != "Config":
        raise ValueError("Expected <Config> root")
    room = root.find("./RoomHostHttp")
    auth = root.find("./Websocket")
    if room is None or auth is None:
        raise ValueError("Missing RoomHostHttp or Websocket field")
    room_host = room.attrib.get("url", "")
    room_port = int(room.attrib.get("port", "0"))
    auth_url = urlparse(auth.attrib.get("url", ""))
    if not room_host.endswith(".miniworldgame.com") or not auth_url.hostname or not auth_url.hostname.endswith(".miniworldgame.com"):
        raise ValueError("Unexpected domain in supplied client XML")
    if not 1 <= room_port <= 65535 or not 1 <= (auth_url.port or 0) <= 65535:
        raise ValueError("Invalid candidate port")
    return {"room_host": room_host, "auth_host": auth_url.hostname,
            "room_port": room_port, "auth_port": auth_url.port}

def compare_catalog(xml_directory: Path) -> list[dict]:
    if not xml_directory.is_dir():
        raise NotADirectoryError(str(xml_directory))
    rows: list[dict] = []
    for code, expected in REGIONS.items():
        path = xml_directory / expected.source_file
        if not path.exists():
            rows.append({"region": code, "status": "missing", "source_file": expected.source_file})
            continue
        try:
            observed = inspect_xml(path)
            match = all(observed[k] == getattr(expected, k) for k in observed)
            rows.append({"region": code, "status": "match" if match else "mismatch",
                         "source_file": expected.source_file, "observed": observed})
        except (ValueError, ElementTree.ParseError, OSError) as exc:
            rows.append({"region": code, "status": "invalid",
                         "source_file": expected.source_file, "reason": type(exc).__name__})
    return rows

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline Global 1.7.15 XML candidate comparison")
    parser.add_argument("directory", type=Path, help="Local directory containing serverlist*.xml")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout")
    args = parser.parse_args(argv)
    rows = compare_catalog(args.directory)
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        for row in rows:
            print(f'{row["region"]:10s} {row["status"]:10s} {row["source_file"]}')
    print("Offline comparison only: matches DO NOT prove active servers or valid Global login.", 
          file=__import__("sys").stderr)
    return 1 if any(r["status"] in {"invalid", "mismatch"} for r in rows) else 0

if __name__ == "__main__":
    raise SystemExit(main())
