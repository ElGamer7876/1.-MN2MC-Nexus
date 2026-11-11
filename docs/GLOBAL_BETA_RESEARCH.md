# Global 1.7.15 BETA research / 国际版研究

## Project policy

Mini World China 1.58.0 is the default upstream bridge. Global 1.7.15 is an **opt-in BETA**, with a separate UDP listener and provisional packet adapter. **Functional Global multiplayer, password login and room registration are NOT implemented or verified.**

## GitHub research reviewed November 2026

| Project | What it supports | Nexus use / limitations |
|---|---|---|
| [MiniWorld-Lua-Toolkit](https://github.com/ballbomb/MiniWorld-Lua-Toolkit) | Exact Global 1.7.15 resource archive unpacking and Lua 5.1 script analysis | Research only; general code license not established |
| [MiniWorldPkgUnpacker](https://github.com/functy23/MiniWorldPkgUnpacker) | MIT; Global 1.7.x resource containers and asset metadata | Can use MIT tool with attribution, but **do not commit proprietary game assets** |
| [DecodeFullMW](https://github.com/LeMinhVoid-VnxD/DecodeFullMW) | Overseas client XML, region configurations and reverse-engineering notes | Source of candidate host metadata only; provenance below |
| [mwc-patch](https://github.com/sang765/mwc-patch) | Android Global 1.7.15 client, versionCode 67343 and client-side message references | Research only; do not copy anti-ban, identity spoofing or exploit patches |
| [MnMCP archived](https://github.com/NDBlockConnect/Minecraft.and.MiniWorldCreata-CrossPlatform-CrossPlay) | Experimental Minecraft/China Mini World bridge | Architecture reference, NOT proof of Global interoperability |
| [MnChat](https://github.com/ReYueY1ng/MnChat), [MiniProtocol](https://github.com/xiaohe123awa/miniprotocol) | Chinese authentication/chat protocols | China-only source study; do not send Global passwords to their Chinese endpoints |

The candidate Global room/account domains are extracted from client resource files at:
https://github.com/LeMinhVoid-VnxD/DecodeFullMW/tree/ee97d7f4df5ee166721542889b371155055f0b69/03_Nguon_MiniWorld_OverseasGame/04_Tai_Nguyen_first_res/script/conf/10

These historic client-side XML files specify **RoomHostHttp port 8080** and an account/Websocket host **port 4000**. They **do not** confirm current reachability, a working password API, official 1.7.15 login compatibility, or a player's region. Do not assume an HTTP-looking URL can safely receive passwords.

## Safe stage gates

1. **Implemented:** opt-in Global BETA profile, independent listener, offline region metadata, provisional legacy-shaped packet decoding; China remains the default.
2. **Not implemented:** Global 1.7.15-specific protocol schema, client handshake and verified cltversion; requires sanitized, authorized fixtures.
3. **Not implemented:** Global password login, authorized account-region validation, room discovery/hosting. No assumed endpoint, no Chinese credential fallback.
4. **Not implemented:** gameplay proofs (join, movement, chat, blocks, inventory, entities) with Paper 1.21.11.
5. **Not implemented:** real expansion of official Global rooms and synchronization of data across them.

Useful offline commands:

    .venv/bin/python main.py --dry-run
    .venv/bin/python main.py --list-regions
    .venv/bin/python main.py --mode global --dry-run
    .venv/bin/python -m pytest -q tests/test_global_beta_regions.py

Avoid public uploads of access tokens, passwords, session cookies, raw PCAP files or other players' identifiers. Reuse independently licensed code with attribution, not decompiled game binaries or assets.

## 简体中文

默认主线为迷你世界中国版 **1.58.0**；国际版 **1.7.15 BETA** 仅能手动启用，目前没有经过验证的真实国际版登录、房间创建或跨游戏联机能力。

研究参考：MiniWorld-Lua-Toolkit（明确提到 1.7.15 Lua）、MiniWorldPkgUnpacker（MIT，国际版 1.7.x 资源）、DecodeFullMW（候选区域 XML）、mwc-patch（安卓 1.7.15）、MnChat/MiniProtocol（仅中国版）。客户端 XML 端口及主机名称并非官方登录 API 的证明，也不能证明服务当前在线。不要将游戏原始资源、密码或会话信息提交到开源代码仓库。
