# Edition runtime / 版本运行说明

## English

MN2MC-Nexus now offers three independent runtime modes:

| Mode | Command | UDP port | Compatibility |
|---|---|---|---|
| Global only (default) | python main.py | 11155 | Experimental, UNVERIFIED |
| China only | python main.py --mode china | 11156 | Upstream 1.58.0 translation baseline |
| Both | python main.py --mode both | 11155 and 11156 | Independent processes |

Run python main.py --dry-run to print the planned listeners without making network connections. Use --port 12000 to override a single-edition listener. The both mode rejects duplicate ports.

Set nexus.runtime.mode in config.yaml to global, china or both to make the selection persistent. The global_port and china_port values can also be configured there. Each edition runs in its own Python process to avoid sharing the protocol version, room state, game account or packet handlers.

### Global 1.7.15 compatibility status

IMPORTANT: The Global profile currently tries the existing China 1.58.0 Protobuf codec only as an experimental compatibility layer. We have no verified Global 1.7.15 schema, client version field or authenticated Global room publishing API. A packet-guard checks the incoming legacy-shaped envelope and rejects malformed packets, but that does not prove semantic compatibility or working crossplay. The local listener does NOT register rooms on Mini World Global servers. In Global mode, Chinese mini1.cn room creation and login are forcibly disabled. Global account credentials must never be sent to the Chinese endpoints.

The Android 1.7.15 build versionCode reported by a community APK project is not sufficient to identify the game's real network cltversion. Do not fill global_client_version_code with an unverified value.

To complete real Global support we need authorized test captures with version and message-code metadata, Global room discovery/login response schemas, and semantic mappings for chat, movement, chunks, blocks and entities. Never upload raw tokens, passwords, cookies or identifiers. All samples should be sanitized. Regional account boundaries, rate limits and game terms must be respected.

### Original China mode

China 1.58.0 is kept separately. Its existing room host and optional intercept workflow are retained if configured; see docs/UPSTREAM_README.zh-CN.md. Global remains the default even when a China account is configured. When running both, configure distinct local ports and point each separate client at its own listener.

## 简体中文

MN2MC-Nexus 默认运行实验性国际版 1.7.15 监听器（UDP 11155）。使用 python main.py --mode china 运行原来的中国版 1.58.0（UDP 11156），或者 python main.py --mode both 同时运行两个独立进程；使用 --dry-run 只查看配置。

可在 config.yaml 的 nexus.runtime.mode 中设置 global / china / both，配置 global_port、china_port。两个版本独立运行，不共享游戏账号、房间状态和 Protobuf 全局变量。

**重要：国际版跨游戏联机尚未验证可用。** 目前国际版仅通过独立适配层实验性复用中国版 1.58.0 的消息结构，并增加严格的包头校验；实际消息 ID、登录流程、地图同步和进房方式都需要进一步测试。国际版不调用中国区 mini1.cn 的登录/创建房间 API，也不会自动在国际版大厅中创建房间。安卓 APK versionCode 不能直接当作游戏网络 cltversion。请只在授权的本地环境测试，并对调试数据脱敏处理。
