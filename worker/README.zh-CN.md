# MN2MC-Nexus Worker

[English](README.md) | [简体中文](README.zh-CN.md)

此服务位于 **web 分支**，使用 FastAPI 和 MySQL 存储房间人数、状态及候选地区信息。**不负责登录 Mini World、创建真实游戏房间或自动同步地图**。地区地址尚待验证。

## 安装和部署

需要 Python 3.13+、MySQL 8.0+ 或兼容的 MariaDB。推荐在 Debian VPS 部署，或者支持长期运行 Python 进程的托管平台。

    cd worker
    python -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt

建立独立数据库，应用 schema.sql，然后通过安全环境变量配置 MYSQL_HOST、MYSQL_PORT、MYSQL_DATABASE、MYSQL_USER、MYSQL_PASSWORD 和至少 32 字符的 NEXUS_API_TOKEN。不要把密码放入 Git。启动：

    uvicorn app.main:app --host 127.0.0.1 --port 8080

请使用 HTTPS 反向代理，不要公开 MySQL 端口。此 Worker 不储存游戏密码和游戏登录令牌，仅保存配置的账号**别名**。

接口：GET /health、GET /regions、GET /rooms?region=usz 和需 Bearer Token 的 PUT /rooms/usz/room-001。PUT 请求体例子：

    {"account_alias":"usz-host-1","players":40,"capacity":40,"status":"full"}

数据库使用 UNIQUE(region, account_alias) 防止同一账号重复占用本地区房间。每间最多 40 人属于规划上限，不代表官方允许超额建房。正式跨区登录、国际版真实房间创建及跨房间进度同步仍需独立实现与测试。
