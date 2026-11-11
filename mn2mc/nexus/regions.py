"""Offline catalog of Global endpoint CANDIDATES from client XML.

NOT official authentication API documentation. Never treat reachability as
permission, as successful login, or as evidence a region accepts an account.
"""
import asyncio
from collections.abc import Awaitable, Callable, Collection
from dataclasses import dataclass

# Provenance: LeMinhVoid-VnxD/DecodeFullMW, client resources,
# 03_Nguon_MiniWorld_OverseasGame/04_Tai_Nguyen_first_res/script/conf/10/
# Imported as short host facts, not copied game assets.
SOURCE_URL = (
    "https://github.com/LeMinhVoid-VnxD/DecodeFullMW/tree/"
    "ee97d7f4df5ee166721542889b371155055f0b69/"
    "03_Nguon_MiniWorld_OverseasGame/04_Tai_Nguyen_first_res/script/conf/10"
)

@dataclass(frozen=True)
class Region:
    code: str
    room_host: str
    auth_host: str
    room_port: int = 8080
    auth_port: int = 4000
    source_file: str = ""
    verified_login: bool = False

REGIONS: dict[str, Region] = {
    "overseas": Region("overseas", "openroom.miniworldgame.com", "acchm.miniworldgame.com", source_file="serverlist.xml"),
    "usz": Region("usz", "openroom-usz.miniworldgame.com", "acchm-usz.miniworldgame.com", source_file="serverlist_usz.xml"),
    "hkz": Region("hkz", "openroom-hkz.miniworldgame.com", "acchm-hkz.miniworldgame.com", source_file="serverlist_hkz.xml"),
    "jpz": Region("jpz", "openroom-jpz.miniworldgame.com", "acchm-jpz.miniworldgame.com", source_file="serverlist_jpz.xml"),
    "brz": Region("brz", "openroom-brz.miniworldgame.com", "acchm-brz.miniworldgame.com", source_file="serverlist_brz.xml"),
    "ruz": Region("ruz", "openroom-ruz.miniworldgame.com", "acchm-ruz.miniworldgame.com", source_file="serverlist_ruz.xml"),
    "gerz": Region("gerz", "openroom-gerz.miniworldgame.com", "acchm-gerz.miniworldgame.com", source_file="serverlist_gerz.xml"),
    "vnz": Region("vnz", "openroom-vnz.miniworldgame.com", "acchm-vnz.miniworldgame.com", source_file="serverlist_vnz.xml"),
    "thz": Region("thz", "openroom-thz.miniworldgame.com", "acchm-thz.miniworldgame.com", source_file="serverlist_thz.xml"),
    "sgpz": Region("sgpz", "openroom-sgpz.miniworldgame.com", "acchm-sgpz.miniworldgame.com", source_file="serverlist_sgpz.xml"),
    "inaz": Region("inaz", "openroom-inaz.miniworldgame.com", "acchm-inaz.miniworldgame.com", source_file="serverlist_inaz.xml"),
    "twz": Region("twz", "openroom-twz.miniworldgame.com", "acchm-twz.miniworldgame.com", source_file="serverlist_twz.xml"),
    "ussz": Region("ussz", "openroom-us_sz.miniworldgame.com", "acchm-us_sz.miniworldgame.com", source_file="serverlist_ussz.xml"),
    "brnz": Region("brnz", "openroom-brnz.miniworldgame.com", "acchm-brnz.miniworldgame.com", source_file="serverlist_brnz.xml"),
}
DEFAULT_ORDER = tuple(REGIONS)
# Country names are NOT regional codes; do not silently use these as accounts.
INDEPENDENT_AREAS = ("russia", "europe_except_spain", "brazil")

class RegionNotConfigured(ValueError):
    pass

class NoUsableRegion(RuntimeError):
    pass

async def select_region(
    probe: Callable[[Region], Awaitable[bool]],
    account_regions: Collection[str],
    mode: str = "auto",
    *,
    timeout: float = 5.0,
    order: tuple[str, ...] = DEFAULT_ORDER,
) -> Region:
    """Select a *candidate host* with a configured account alias.

    Injected probe must be NON-authenticating, and MUST NOT send credentials.
    Availability does not mean a login, a valid room or Global 1.7.15 support.
    """
    if not 0 < timeout <= 60:
        raise ValueError("Timeout must be 0 < timeout <= 60")
    accounts = set(account_regions)
    if not accounts <= REGIONS.keys():
        raise ValueError("Unknown region code in account configuration")
    if mode in INDEPENDENT_AREAS:
        raise RegionNotConfigured("Use a specific candidate region code, not a geographic label")
    if mode == "auto":
        if not order or len(order) != len(set(order)) or any(k not in REGIONS for k in order):
            raise ValueError("Invalid region order")
        candidates = tuple(k for k in order if k in accounts)
    elif mode in REGIONS:
        if mode not in accounts:
            raise RegionNotConfigured("An account for the selected candidate region is required")
        candidates = (mode,)
    else:
        raise ValueError("Unknown region")
    for code in candidates:
        try:
            if await asyncio.wait_for(probe(REGIONS[code]), timeout=timeout) is True:
                return REGIONS[code]
        except (TimeoutError, OSError, ConnectionError):
            continue
    raise NoUsableRegion("No reachable configured candidate; no login attempted")
