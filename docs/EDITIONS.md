# Edition runtime / 版本运行

## English

**China 1.58.0 is the default**, retaining the upstream protocol bridge to Minecraft Java 1.21.11. **Global 1.7.15 BETA must be opted into** and is currently an unverified local listener, not functional Global crossplay.

| Mode | Command | UDP port | Scope |
|---|---|---|---|
| China (default) | python main.py | **11155** | Existing upstream China translator |
| China explicit | python main.py --mode china | **11155** | Same |
| Global BETA only | python main.py --mode global | **11156** | Provisional packet compatibility experiment |
| Both | python main.py --mode both | **11155, 11156** | Separate processes; no shared sessions |

View an offline execution plan with python main.py --dry-run; print candidate Global host facts without making network requests using python main.py --list-regions. Single-edition ports can be overridden with --port 12000; both mode requires distinct ports.

Persistent configuration:

    nexus:
      runtime:
        mode: china
        global_beta_enabled: false
        china_port: 11155
        global_port: 11156
        global_client_version_code: null

**Existing settings:** Older local config.yaml may still contain mode: global. Without explicit global_beta_enabled: true, the program deliberately starts China instead. The setup wizard asks whether to add Global BETA; choosing yes sets mode: both and global_beta_enabled: true. An explicit --mode global or --mode both on the command line also opts into beta for that launch. For persistent Global-only beta, set mode: global and global_beta_enabled: true.

### Compatibility and interception

The China 1.58.0 adapter preserves its existing handlers, room hosting and authentication options when configured. The China-only tools/mitm.py now targets UDP **11155** by default. If you override the China port, set environment MN2MC_CHINA_PORT to the same value.

Global BETA only reuses a **provisional China 1.58.0-shaped packet envelope**; no 1.7.15 schema, handshake, authenticated room listing, password login or actual gameplay interoperability has been verified. The community Android versionCode **67343** is NOT the network cltversion. Global BETA never sends passwords to China endpoints and cannot be found automatically by the Mini World Global public lobby. China and Global run separate Python processes with distinct ports and do not share accounts.

Research references: [GLOBAL_BETA_RESEARCH.md](GLOBAL_BETA_RESEARCH.md), [REGIONS.md](REGIONS.md).

## 简体中文

默认启动**中国版 1.58.0**，监听 UDP **11155**。国际版 **1.7.15 BETA** 需要手动选择，监听 UDP **11156**，目前尚不能确认成功登录、创建房间或进行跨游戏联机。--mode both 会启动独立的两个进程。

    python main.py --dry-run
    python main.py --mode china
    python main.py --mode global
    python main.py --mode both
    python main.py --list-regions

旧配置如果 mode 为 global 但未设置 global_beta_enabled: true，将安全地回到中国版。中国区 tools/mitm.py 默认使用 UDP 11155。上述国际版主机、Protobuf 消息及数据均为研究候选信息，不能把客户端 build versionCode 当成实际网络 cltversion。
