# CachyOS installer / CachyOS 安装向导

## English

On the GitHub main branch, as your normal user (not root):

    bash install-cachyos.sh --dry-run
    bash install-cachyos.sh

The installer prepares uv/Python 3.13, Node.js and dependencies, with an optional local Paper 1.21.11 download. **China 1.58.0 is the default.** The wizard asks whether to enable experimental **Global 1.7.15 BETA** too. Answer **N** for China only: no Global UID or password is requested. Answer **Y** for both China and Global in independent processes; only then enter your Global UID and candidate region code for planning.

- China default: python main.py (UDP 11155).
- Global BETA explicit: python main.py --mode global (UDP 11156).
- Both explicit: python main.py --mode both.
- Region metadata listing (offline): python main.py --list-regions.

The installer makes config.yaml mode 0600. **Global password authentication is NOT implemented**; it does not request or transmit a password. Authenticator retry logic is for a future audited provider. Never reuse Chinese auth endpoints for a Global account.

Paper is local-only and offline-mode is **not** appropriate for a public server; you must review/accept the Minecraft EULA before running it. See [EDITIONS.md](EDITIONS.md).

## 简体中文

普通用户执行 bash install-cachyos.sh，主线默认**中国版 1.58.0（UDP 11155）**。安装器会询问是否额外启用**国际版 1.7.15 BETA（UDP 11156）**；不启用无需提供国际版 UID；启用后仅填写 UID 和地区代码，用于本地配置，并不会真实登录。

国际版密码 API 尚未验证，因此不采集密码；国际版真正连接和发布房间尚未实现。可选安装 Paper 1.21.11 用于受控本地试验，需自行接受 EULA。
