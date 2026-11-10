# MN2MC-Nexus Worker

[English](README.md) | [简体中文](README.zh-CN.md)

**Development branch:** web. Separate FastAPI/MySQL status service for room occupancy and region metadata. It does **not** host Mini World rooms, authenticate player accounts, or synchronize game worlds. All regional hostnames are still research candidates. The worker can run on your Debian VPS or a Python-capable managed host.

## Setup

Requires Python 3.13+, MySQL 8.0+ (or compatible MariaDB) and the worker-only Python dependencies. Prefer a dedicated MySQL user with SELECT/INSERT/UPDATE rights only to this database; provision the schema separately with an administrator account.

    cd worker
    python -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt

Create a database, apply schema.sql and set MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD and NEXUS_API_TOKEN as environment variables. Do not commit the credentials or include them in URLs. Read .env.example for examples. Start:

    uvicorn app.main:app --host 127.0.0.1 --port 8080

Put an HTTPS reverse proxy in front of the service before using it publicly; never expose the MySQL port to the internet. This service does not handle authentication tokens from the game. Use your own API token only.

## Endpoints

- GET /health: web service state (not a database connectivity guarantee)
- GET /regions: known candidate regions and unverified independent areas
- GET /rooms?region=usz: room occupancy/status
- PUT /rooms/usz/room-001: protected status upsert, Authorization: Bearer YOUR_API_TOKEN

Example PUT JSON body:

    {"account_alias":"usz-host-1","players":40,"capacity":40,"status":"full"}

MySQL stores *account aliases*, not passwords or game tokens. The unique(region, account_alias) constraint enforces one room per account in each region. Every region requires its own authorized account. A capacity of 40 is a configurable room limit, not an official API entitlement or permission to evade service limits. Status reports should come only from authorized room hosts.

## Deployment notes

For hosts with only 0.5 vCPU and 4 GB RAM, keep worker count at 1, MySQL connection pool at 3 and throttle upstream publishers. Monitor CPU usage and memory; shared providers may suspend idle applications. Full region login and real Global room creation must be implemented and verified separately, then connected to this status API.

## Hostly deployment: fix for Nothing to run

Do not run the upstream Minecraft Node.js package as a website. Select branch web from repository root and choose Dockerfile/Docker build instead of Node.js autodetection. The Dockerfile installs worker/requirements.txt and serves site/ at / and the FastAPI service under /api/. It honors PORT (default 8080).

Expected routes after deployment: https://git.hostlyus.com/, https://git.hostlyus.com/api/, /api/health, /api/regions and /api/rooms. GitHub Pages alternative: https://elgamer7876.github.io/1.-MN2MC-Nexus/ . Select Settings > Pages > Source: GitHub Actions. Keep MySQL and API token secrets within Hostly; never put them in browser code.
