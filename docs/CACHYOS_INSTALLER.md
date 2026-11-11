# CachyOS interactive installer / CachyOS 交互式安装器

## English

On the main branch, run:

    bash install-cachyos.sh --dry-run
    bash install-cachyos.sh

The installer prepares Python 3.13, Node.js, MN2MC-Nexus bridge dependencies and asks for a Global UID, account region and optional China 1.58.0 process. config.yaml is stored with mode 0600. Optionally download official stable Paper 1.21.11 and verify its published checksum. The local Paper server requires accepting the EULA explicitly, and offline-mode is for isolated localhost tests only.

**Important:** No independently verified official Global 1.7.15 password authentication API is known. The installer therefore does NOT request a password it cannot validate. It cannot log into Global or register a public room yet. Sign in through the official game client. The code in mn2mc/nexus/global_auth.py contains the future masked password prompt, with up to three retries only on a verified invalid-password response. Network errors and rate limits do not cause automatic password retries.

Do not send a password to guessed regional endpoints, upload one to GitHub or store it in Hostly. Global crossplay remains experimental.

## 简体中文

在 main 分支运行 bash install-cachyos.sh。安装器自动安装 Python 3.13、Node.js 及依赖，询问国际版 UID、账号区域以及是否启用中国版；可选安装 Paper 1.21.11 本地服务器。配置文件仅在本机保存，不保存密码。

**重要：** 尚未验证国际版 1.7.15 官方密码登录接口。安装器不会收集不能验证的密码，也无法真实登录国际版或发布房间。请先使用官方游戏客户端登录。已经预留密码隐藏输入和最多三次错误密码重试接口，待安全、经过验证的登录功能开发后启用。
