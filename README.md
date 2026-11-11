# MN2MC-Nexus

**Edition runtime:** Global 1.7.15 is the default *experimental* local listener (UDP 11155). Use --mode china to run the original Chinese 1.58.0 bridge (UDP 11156), or --mode both to start both independently. Use python main.py --dry-run before launching. See [edition guide](docs/EDITIONS.md). **Global is NOT verified or publicly room-hostable yet.**

[English](README.md) | [简体中文](README.zh-CN.md)

**An extensible Mini World–Minecraft protocol bridge for third-party mods, regional routing and future multiplayer networks.**

> **Experimental fork of [ReYueY1ng/MN2MC](https://github.com/ReYueY1ng/MN2MC).** The existing translation code targets Mini World China **1.58.0** and Minecraft Java **1.21.11**. Mini World Global **1.7.15**, regional login, automatic remote room creation, cross-room syncing and Velocity networking have **not been verified or implemented end-to-end**.

## What Nexus adds

- Keeps upstream chat, block, inventory, item, entity, movement and session handlers.
- Opt-in hooks for outgoing chat and numeric block-ID mappings. Third-party mods need explicit adapters and version-specific testing.
- Account-aware region discovery: examines eligible regions without automatically signing in or copying credentials between regions.
- Per-region capacity planning: one account alias per room, up to **40 players per room**. When full, an optional room provider can allocate the next unused account **of that same region**. The library never generates accounts or bypasses authorization.
- Separate MySQL worker development in the [web branch](../../tree/web); server status, regional capacities and network coordination are goals, not a deployed production service.

## Global region choices (proposed)

| Region | Room endpoint candidate | Suggested location/language |
|---|---|---|
| Overseas | openroom.miniworldgame.com | International |
| USZ | openroom-usz.miniworldgame.com | United States (English), Mexico (Spanish) |
| HKZ | openroom-hkz.miniworldgame.com | Hong Kong (Chinese), Vietnam (Vietnamese) |
| JPZ | openroom-jpz.miniworldgame.com | Japan (Japanese) |
| Independent (no verified endpoints) | Unavailable | Russia, Brazil, Europe excluding Spain |

These are **maintainer-provided hypotheses**, not proven official geographic assignments or login endpoints. Each selected region **requires an account belonging to that region**. In auto mode, the first reachable region with an existing account is selected, but **login remains a separate user-authorized operation**. Other independent regions cannot be used until their real endpoints are verified. The eight room/auth host candidates and full details appear in [docs/REGIONS.md](docs/REGIONS.md).

## When a 40-player room is full

The independent RoomPool module plans **one room per account**, separately for each region:

| Example region | Configured accounts | Max planned rooms | Max planned players |
|---|---:|---:|---:|
| USZ | 3 | 3 | 120 |
| HKZ | 2 | 2 | 80 |
| JPZ | 1 | 1 | 40 |

A real room is created **only** when an authorized, tested room-creation callback is configured. Until Global 1.7.15 login and hosting APIs are validated, this is capacity orchestration, not an active automatic room host. Separate rooms **do not automatically share maps, inventory, chat or progression**. Multiple-account use must comply with game terms.

## Installation of existing China bridge

Requires Python 3.13+, Node.js and upstream dependencies.

    python -m pip install -r requirements.txt
    npm install
    python main.py

The original server and proxy setup is kept in [upstream Chinese README](docs/UPSTREAM_README.zh-CN.md). On first startup, config.yaml is generated. The Nexus options under the nexus section include region_mode, region_accounts (alias lists, never passwords), auto_expand_rooms, room_capacity and plugins. Only trusted local Python plugin module names should be added to plugins; extensions are **not sandboxed**. See [example](examples/nexus_chat_and_blocks.py).

## Development status and safety

- Region selector, room pool and opt-in chat/block mapping hooks: implemented as Python modules.
- Global login and regional network connectivity probes: not implemented; host and protocol verification pending.
- Production auto-spawn of Global rooms and multi-server state synchronization: not implemented; audited regional sessions and server authorization required.
- MySQL worker: maintained on the web branch.
- Compliance: avoid credential sharing, CAPTCHA or ban evasion, abuse of multiple accounts and unauthorized game-server access.

**MIT License.** Preserve the original ReYueY1ng 2026 copyright and notices. MN2MC-Nexus is an unofficial independent fork; the game may apply anti-cheat and service restrictions.
