# Region routing and room planning / 区域路由与房间规划

## English

The following hostnames were supplied by the maintainer. They are **candidate hosts** and have not been established as authenticated login URLs for Mini World Global 1.7.15. Geographical associations are suggestions, not official verified server assignments.

| Region | Open-room candidate | Authentication host candidate | Suggested areas |
|---|---|---|---|
| Overseas | openroom.miniworldgame.com | acchm.miniworldgame.com | International |
| USZ | openroom-usz.miniworldgame.com | acchm-usz.miniworldgame.com | English: United States; Spanish: Mexico |
| HKZ | openroom-hkz.miniworldgame.com | acchm-hkz.miniworldgame.com | Chinese: Hong Kong; Vietnamese: Vietnam |
| JPZ | openroom-jpz.miniworldgame.com | acchm-jpz.miniworldgame.com | Japanese: Japan |

**Independent areas:** Russia, Brazil and Europe (except Spain). No verified hosts for these areas are known. The server assignment of Spain has not been confirmed. They cannot yet be auto-selected.

**Auto region selection:** Nexus receives a list of existing region-specific account aliases, and a separate **non-authenticating** reachability probe. It checks Overseas, USZ, HKZ and JPZ in order, skipping regions with no account. It returns the first reachable candidate. **The operator still needs a separate account and separately authorized login for that region.** There is no automatic regional login, credential exchange or region-bypass logic.

**When a room becomes full:** Each account can own at most one active room in its region. The RoomPool module can ask a separately authenticated, operator-authorized create_room callback to provision the next 40-player room for another unused account of the **same region**. Its maximum capacity equals the number of configured accounts times the room capacity (up to 40). If no spare account is available, no room is created. The callback is not yet implemented for real Global servers. Different rooms do not share world state, player inventories or progression. Avoid abusive/disruptive multi-account activities.

## 简体中文

以下地址由维护者提供，目前属于**候选主机**，尚未验证为国际版 1.7.15 的官方登录接口。地区分配是建议，不是官方确认结果。

| 区域 | 房间候选地址 | 认证候选地址 | 建议地区 |
|---|---|---|---|
| Overseas | openroom.miniworldgame.com | acchm.miniworldgame.com | 国际通用 |
| USZ | openroom-usz.miniworldgame.com | acchm-usz.miniworldgame.com | 美国（英语）、墨西哥（西班牙语） |
| HKZ | openroom-hkz.miniworldgame.com | acchm-hkz.miniworldgame.com | 香港（中文）、越南（越南语） |
| JPZ | openroom-jpz.miniworldgame.com | acchm-jpz.miniworldgame.com | 日本（日语） |

**独立地区：** 俄罗斯、巴西、除西班牙外的欧洲地区。目前缺少经过验证的服务器地址；西班牙实际分区也未确定，暂时不能自动选择。

**自动选区：** 先配置已有的地区账号别名，再由独立的**非登录**探测程序按 Overseas、USZ、HKZ、JPZ 顺序检查，只考虑拥有该地区账号的区域。返回第一个可连接地区，**但用户仍需使用该地区独立账号及授权登录流程**。不会跨区域使用密码或绕过限制。

**满员扩容：** 每个地区账号最多对应一间房。达到 40 人时，RoomPool 可通过单独验证且经过授权的 create_room 回调，使用**同区域**未被占用的另一个账号创建新房。最大规划容量为该地区账号数乘以单间房人数（上限 40）。没有空闲账号就不会创建。国际版真实创建接口尚未实现。不同房间不会自动同步地图、背包、聊天和进度。不得滥用多账号。
