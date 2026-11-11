# MN2MC-Nexus

**版本：** 默认实验性国际版 1.7.15 监听器（11155 UDP），使用 python main.py --mode china 启用中国版 1.58.0（11156 UDP），使用 python main.py --mode both 独立运行两者。参见 [说明](docs/EDITIONS.md)。国际版的实际跨游戏联机与登录仍未验证。


[English](README.md) | [简体中文](README.zh-CN.md)

**支持第三方模组、区域路由与未来多人服务器网络的可扩展 Mini World–Minecraft 协议桥接项目。**

> **实验性分叉**，基于 [ReYueY1ng/MN2MC](https://github.com/ReYueY1ng/MN2MC)。现有上游代码面向中国版 **1.58.0** 与 Minecraft Java **1.21.11**。国际版 **1.7.15**、区域登录、真实房间自动扩容、跨房间数据同步和 Velocity 网络**尚未实现端到端验证**。

## 本分叉新增功能

- 保留上游聊天、方块、物品、背包、实体、移动和会话处理。
- 可选可信插件：出站聊天修改和数值方块 ID 映射。第三方模组仍需要针对版本测试。
- 依据已有地区账号检查可用服务器；不自动登录或跨区域复制凭据。
- 按地区规划房间：**每个账号对应一间房，每间最多 40 人**。满员后可通过授权、已经验证的回调，分配同区域另一个未使用的账号创建下一间房。不会自动创建账号或绕过认证。
- MySQL Worker 在 [web 分支](../../tree/web) 开发；跨服务器协调尚未部署。

## 国际区域选择（候选）

| 区域 | 房间候选主机 | 建议国家/语言 |
|---|---|---|
| Overseas | openroom.miniworldgame.com | 国际通用 |
| USZ | openroom-usz.miniworldgame.com | 美国（英语）、墨西哥（西班牙语） |
| HKZ | openroom-hkz.miniworldgame.com | 香港（中文）、越南（越南语） |
| JPZ | openroom-jpz.miniworldgame.com | 日本（日语） |
| 独立区域（主机未验证） | 未知 | 俄罗斯、巴西、西班牙以外的欧洲 |

以上地域关系由维护者提供，**不是已验证的官方登录路由**。选择某地区**需要该地区的账号**。自动模式仅能选择已经配置账号且可连接的地区；**不会替用户自动登录**。独立地区需要先核实实际服务器域名。全部八个房间/认证候选主机及详细说明见 [docs/REGIONS.md](docs/REGIONS.md)。

## 房间满员后自动扩容

RoomPool 模块按地区独立配置：例如 USZ 有 3 个账号，最多规划 3 间房（120 人）；HKZ 有 2 个账号，对应 2 间房（80 人）；JPZ 有 1 个账号，对应 1 间房（40 人）。

真实房间只有通过已验证、已授权的创建接口才能启动。国际版 1.7.15 的实际认证和房间创建 API 仍待研究，因此目前是**容量管理框架**，不是可直接运行的国际版自动房间服务器。房间间的地图、背包、聊天和进度**不会自动同步**。使用多账号必须遵守游戏规则。

## 运行现有中国版桥接

需安装 Python 3.13+、Node.js 及原项目依赖：

    python -m pip install -r requirements.txt
    npm install
    python main.py

原来的安装及服务器设置说明保存在 [原版中文 README](docs/UPSTREAM_README.zh-CN.md)。首次运行生成 config.yaml。nexus 配置含 region_mode、region_accounts（仅账号别名、不能存密码）、auto_expand_rooms、room_capacity 与 plugins。插件必须是可信的本地 Python 模块，执行时**没有沙盒保护**。示例见 [插件代码](examples/nexus_chat_and_blocks.py)。

## 状态、许可和安全

区域选择模块、房间容量管理、聊天与方块映射扩展接口已提交。国际版真实登录、探测接口、自动真实房间创建与跨区同步还未完成验证。MySQL Worker 在 web 分支独立开发。请勿共享账号密码、绕过验证码或封禁、滥用多账号，或未经授权访问服务器。

采用 **MIT License**，保留原作者 ReYueY1ng（2026）的版权和署名。本项目为非官方分叉，协议翻译可能触发反作弊或服务限制。
