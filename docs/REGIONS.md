# Global BETA regions / 国际版候选区域

The following domain pairs are extracted from [Overseas client resource XML](https://github.com/LeMinhVoid-VnxD/DecodeFullMW/tree/ee97d7f4df5ee166721542889b371155055f0b69/03_Nguon_MiniWorld_OverseasGame/04_Tai_Nguyen_first_res/script/conf/10). They are **unverified candidates**, not documented public login APIs. Every room host below has XML port **8080**, and the respective account/WebSocket host has XML port **4000**. Port values describe the client resources, not supported public credential submission.

| Code | Room host candidate | Account/WebSocket candidate | XML filename |
|---|---|---|---|
| overseas | openroom.miniworldgame.com | acchm.miniworldgame.com | serverlist.xml |
| usz | openroom-usz.miniworldgame.com | acchm-usz.miniworldgame.com | serverlist_usz.xml |
| hkz | openroom-hkz.miniworldgame.com | acchm-hkz.miniworldgame.com | serverlist_hkz.xml |
| jpz | openroom-jpz.miniworldgame.com | acchm-jpz.miniworldgame.com | serverlist_jpz.xml |
| brz | openroom-brz.miniworldgame.com | acchm-brz.miniworldgame.com | serverlist_brz.xml |
| ruz | openroom-ruz.miniworldgame.com | acchm-ruz.miniworldgame.com | serverlist_ruz.xml |
| gerz | openroom-gerz.miniworldgame.com | acchm-gerz.miniworldgame.com | serverlist_gerz.xml |
| vnz | openroom-vnz.miniworldgame.com | acchm-vnz.miniworldgame.com | serverlist_vnz.xml |
| thz | openroom-thz.miniworldgame.com | acchm-thz.miniworldgame.com | serverlist_thz.xml |
| sgpz | openroom-sgpz.miniworldgame.com | acchm-sgpz.miniworldgame.com | serverlist_sgpz.xml |
| inaz | openroom-inaz.miniworldgame.com | acchm-inaz.miniworldgame.com | serverlist_inaz.xml |
| twz | openroom-twz.miniworldgame.com | acchm-twz.miniworldgame.com | serverlist_twz.xml |
| ussz | openroom-us_sz.miniworldgame.com | acchm-us_sz.miniworldgame.com | serverlist_ussz.xml |
| brnz | openroom-brnz.miniworldgame.com | acchm-brnz.miniworldgame.com | serverlist_brnz.xml |

Other **country-style** domain names appear in serverlist_country.xml (e.g. openroom-br versus openroom-brz). They are not automatically interchangeable. Previously suggested user locations (USZ: USA/Mexico, HKZ: Hong Kong/Vietnam, JPZ: Japan) are **not independently verified account routing rules**. RUZ, BRZ and GERZ are candidate codes that may correspond to geographic areas, not proven account entitlements. Spain's region is not confirmed.

**Behavior:** A separate non-authenticating probe can be injected into select_region(); auto-selection tries ONLY candidate region codes where a matching account alias has already been configured. It returns the first responsive candidate; it does **not** log in, create a real room, grant region access or validate actual 1.7.15 protocol compatibility. Geographic words such as "brazil" are not region codes. In the default China mode no Global discovery runs.

    .venv/bin/python main.py --list-regions
    .venv/bin/python main.py --mode china
    .venv/bin/python main.py --mode global --dry-run

RoomPool has a planning-only limit of up to 40 players per room and one room per authorized account within the same region. Its Global room-creation callback and real cross-room world synchronization do not exist yet.

## 简体中文

以上海外区域主机来自社区客户端 XML，**不是已验证的国际版 1.7.15 官方登录 API**。账号需属于相应区域；可连接不等于允许登录。中国版为默认主线（UDP 11155），国际版 BETA 为自愿启用（UDP 11156）。新增的 RUZ、BRZ、GERZ 等只是候选配置，不能证明这些服务器当前可用，也不能直接向其发送密码。房间自动扩容目前仅为规划框架，不是真实游戏内建房功能。
