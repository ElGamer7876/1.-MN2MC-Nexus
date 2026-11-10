# MN2MC-Nexus website

The same static files serve the main Hostly domain https://git.hostlyus.com/ and GitHub Pages https://elgamer7876.github.io/1.-MN2MC-Nexus/. Public status is served by the Hostly API at https://git.hostlyus.com/api/.

Hostly: deploy the web branch from repository root with the Dockerfile build option, not Node.js autodetection. Apply worker/schema.sql to a dedicated MySQL database and configure MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD and NEXUS_API_TOKEN as secret environment variables.

GitHub Pages: choose Settings > Pages > Source: GitHub Actions. The pages.yml workflow deploys the site directory. If Hostly fails, the static mirror can still load, but live room data will indicate that the API is offline. Browser code must never contain admin API tokens or game account passwords.
