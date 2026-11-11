"use strict";
const messages = {
  en: {
    navFeatures:"Features",navRegions:"Regions",navRooms:"Rooms",navDeploy:"Deploy",
    eyebrow:"OPEN SOURCE · EXPERIMENTAL",
    heroCopy:"A modular Mini World–Minecraft protocol bridge, designed for adapters, community mods and future multiplayer networks.",
    source:"Explore the source",dashboard:"Room dashboard",
    experimental:"China 1.58.0 is the main/default bridge. Global 1.7.15 is an optional BETA; login, room creation and cross-region sync are unverified.",
    moreRegions:"Global BETA candidates also include BRZ, RUZ, GERZ, VNZ, THZ, SGPZ, INAZ, TWZ, USSZ, BRNZ. All login functionality is unverified.",
    platform:"THE PLATFORM",featuresTitle:"Built to be extended.",
    featuresLead:"Keep the original translation engine, add modular capabilities, and work toward server-network interoperability.",
    f1:"Protocol translation",f1d:"The original China 1.58.0 to Minecraft Java 1.21.11 bridge is retained.",
    f2:"Extension hooks",f2d:"Opt-in chat filters and numeric block mapping overrides for trusted local Python modules.",
    f3:"Multiplayer networks",f3d:"Room capacity planning, regional candidates and a MySQL-backed status worker.",
    upstream:"Existing upstream",available:"Implemented module",development:"In development",
    global:"GLOBAL REGIONS",regionsTitle:"Regional discovery.",
    regionsLead:"Region-to-country assignments and endpoints are maintainer-supplied candidates, not verified official login services.",
    int:"International",us:"United States · Mexico",hk:"Hong Kong · Vietnam",jp:"Japan",
    regionsNote:"Independent/unverified areas: Russia, Brazil and Europe excluding Spain. An account from each selected region is required. Auto-select is not auto-login.",
    roomStatus:"ROOM STATUS",roomTitle:"Network overview.",registered:"Registered rooms",
    players:"Reported players",slots:"Available slots",registry:"Room registry",
    filter:"Region",all:"All regions",refresh:"Refresh",
    loading:"Loading API data…",offline:"API unavailable",online:"API connected",
    noRooms:"No rooms reported for this selection.",
    dbError:"The worker responded, but the room database is not ready or configured.",
    roomsError:"Unable to load room status. The Hostly worker may not be deployed yet.",
    roomNote:"Counts come from authorized room operators, not directly from the game. 40 players per room is a planning limit.",
    structure:"INFRASTRUCTURE",deployTitle:"One API. Two frontends.",
    deployLead:"The main Hostly site serves FastAPI and the frontend. GitHub Pages offers a static alternative using the same read-only API.",
    mainSite:"MAIN SITE",mainSub:"Site and FastAPI runtime",
    api:"SHARED API",apiSub:"MySQL room status",alternative:"ALTERNATIVE",ghSub:"Static mirror, same API",
    cta:"Explore the source. Help shape the bridge.",
    ctaText:"Experimental and MIT licensed. Follow development and contribute compatible adapters.",
    docs:"Regional documentation ↗",footer:"Unofficial MIT-licensed fork. Not affiliated with the game's publishers.",
    statusOpen:"Open",statusFull:"Full",statusOffline:"Offline"
  },
  zh: {
    navFeatures:"功能",navRegions:"地区",navRooms:"房间",navDeploy:"部署",
    eyebrow:"开源 · 实验性项目",
    heroCopy:"可扩展的 Mini World–Minecraft 协议桥接系统，面向适配器、社区模组与未来的多人服务器网络。",
    source:"查看源代码",dashboard:"查看房间状态",
    experimental:"中国版 1.58.0 是默认主线；国际版 1.7.15 BETA 为可选功能，登录、真实建房和跨区同步尚未验证。",
    moreRegions:"国际版 BETA 其他候选区：BRZ、RUZ、GERZ、VNZ、THZ、SGPZ、INAZ、TWZ、USSZ、BRNZ；登录均未验证。",
    platform:"核心平台",featuresTitle:"为扩展而设计。",
    featuresLead:"保留原始协议转换功能，添加模块化扩展，并逐步支持多人服务器网络。",
    f1:"协议转换",f1d:"保留中国版 1.58.0 与 Minecraft Java 1.21.11 的原始桥接基础。",
    f2:"扩展接口",f2d:"允许可信本地 Python 模块自定义聊天转换与数字方块 ID 映射。",
    f3:"多人网络规划",f3d:"房间容量管理、国际地区候选配置和 MySQL 状态 Worker。",
    upstream:"保留上游功能",available:"模块已实现",development:"开发中",
    global:"国际地区",regionsTitle:"按区域发现服务器。",
    regionsLead:"地区与国家对应关系、服务器地址均为维护者提供的候选信息，尚未验证为官方登录接口。",
    int:"国际通用",us:"美国 · 墨西哥",hk:"香港 · 越南",jp:"日本",
    regionsNote:"独立地区（地址尚未验证）：俄罗斯、巴西、西班牙以外的欧洲。选择某地区需要该地区账号；自动选区不等于自动登录。",
    roomStatus:"房间状态",roomTitle:"网络概览。",registered:"已登记房间",
    players:"已上报玩家",slots:"剩余位置",registry:"房间列表",
    filter:"地区",all:"全部地区",refresh:"刷新",
    loading:"正在加载 API 数据…",offline:"API 暂不可用",online:"API 已连接",
    noRooms:"该地区目前没有已上报的房间。",
    dbError:"Worker 已响应，但 MySQL 数据库尚未就绪或未配置。",
    roomsError:"无法读取房间状态，Hostly Worker 可能尚未部署。",
    roomNote:"人数来自获得授权的房间管理者上报，不是游戏官方的实时查询。每间 40 人是规划上限。",
    structure:"部署结构",deployTitle:"一个 API，两种前端。",
    deployLead:"Hostly 托管主站和 FastAPI；GitHub Pages 提供使用相同只读 API 的静态备用页面。",
    mainSite:"主站",mainSub:"网站与 FastAPI 服务",
    api:"共享 API",apiSub:"MySQL 房间状态",alternative:"备用网站",ghSub:"静态镜像，使用同一 API",
    cta:"查看源代码，共同完善协议桥接。",
    ctaText:"实验性 MIT 开源项目，欢迎关注开发进度并贡献兼容适配器。",
    docs:"地区配置文档 ↗",footer:"非官方 MIT 开源分叉，与游戏发行方无隶属关系。",
    statusOpen:"开放",statusFull:"已满",statusOffline:"离线"
  }
};
const count = document.getElementById("roomCount");
const players = document.getElementById("playerCount");
const slots = document.getElementById("slotCount");
const list = document.getElementById("roomList");
const status = document.getElementById("apiStatus");
const light = document.getElementById("apiLight");
const filter = document.getElementById("filter");
const refresh = document.getElementById("refresh");
let language = new URLSearchParams(location.search).get("lang") === "zh" ? "zh" : "en";
let currentRooms = null;
const sameHost = ["git.hostlyus.com", "localhost", "127.0.0.1"].includes(location.hostname);
const apiBase = sameHost ? "/api" : "https://git.hostlyus.com/api";
function translate(key) { return messages[language][key] || messages.en[key] || key; }
function setLanguage(next) {
  language = next;
  document.documentElement.lang = next === "zh" ? "zh-CN" : "en";
  document.getElementById("language").textContent = next === "zh" ? "English" : "中文";
  document.querySelectorAll("[data-t]").forEach(el => { el.textContent = translate(el.dataset.t); });
  // All markup here is built-in static content (never fetched from the API).
  document.querySelector("h1").innerHTML = next === "zh" ? "连接世界。<br><em>构建多人网络。</em>" : "Connect worlds.<br><em>Build networks.</em>";
  if (currentRooms) draw(currentRooms);
}
document.getElementById("language").addEventListener("click", () => setLanguage(language === "zh" ? "en" : "zh"));
function element(tag, className, value) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (value !== undefined) el.textContent = String(value);
  return el;
}
function draw(rows) {
  list.replaceChildren();
  if (!rows.length) list.append(element("p", "empty", translate("noRooms")));
  for (const room of rows) {
    const row = element("div", "room-entry");
    const left = element("div");
    left.append(element("strong", "", room.room_id));
    const key = "status" + String(room.status).charAt(0).toUpperCase() + String(room.status).slice(1);
    left.append(element("small", "", String(room.region).toUpperCase() + " · " + translate(key)));
    row.append(left, element("span", "count", String(room.players) + " / " + String(room.capacity)));
    list.append(row);
  }
  count.textContent = String(rows.length);
  players.textContent = String(rows.reduce((n, r) => n + (Number(r.players) || 0), 0));
  slots.textContent = String(rows.reduce((n, r) => n + Math.max(0, Number(r.capacity || 0) - Number(r.players || 0)), 0));
}
async function request(path) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8500);
  try {
    const response = await fetch(apiBase + path, { signal: controller.signal, cache: "no-store" });
    if (!response.ok) {
      const error = new Error("HTTP " + response.status);
      error.statusCode = response.status;
      throw error;
    }
    return await response.json();
  } finally { clearTimeout(timeout); }
}
async function reload() {
  refresh.disabled = true;
  status.textContent = translate("loading");
  try {
    const query = filter.value ? "?region=" + encodeURIComponent(filter.value) : "";
    const data = await request("/rooms" + query);
    if (!Array.isArray(data.rooms)) throw new Error("Unexpected worker response");
    currentRooms = data.rooms;
    draw(currentRooms);
    light.classList.remove("offline");
    status.textContent = translate("online");
  } catch (error) {
    currentRooms = null;
    light.classList.add("offline");
    status.textContent = translate("offline");
    count.textContent = players.textContent = slots.textContent = "—";
    list.replaceChildren(element("p", "empty", error.statusCode === 503 ? translate("dbError") : translate("roomsError")));
  } finally { refresh.disabled = false; }
}
refresh.addEventListener("click", reload);
filter.addEventListener("change", reload);
setLanguage(language);
reload();
