"""Account-aware region discovery; never sends credentials or logs in."""
import asyncio
from collections.abc import Awaitable, Callable, Collection
from dataclasses import dataclass

@dataclass(frozen=True)
class Region:
    code: str
    room_host: str
    auth_host: str

# Host candidates supplied by maintainer: NOT verified official login API URLs.
REGIONS = {
    "overseas": Region("overseas", "openroom.miniworldgame.com", "acchm.miniworldgame.com"),
    "usz": Region("usz", "openroom-usz.miniworldgame.com", "acchm-usz.miniworldgame.com"),
    "hkz": Region("hkz", "openroom-hkz.miniworldgame.com", "acchm-hkz.miniworldgame.com"),
    "jpz": Region("jpz", "openroom-jpz.miniworldgame.com", "acchm-jpz.miniworldgame.com"),
}
DEFAULT_ORDER = ("overseas", "usz", "hkz", "jpz")
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
    """Return first reachable region with a configured region-specific account.

    The injected probe must be NON-authenticating. Reachable != logged in.
    This selector does not exchange credentials or bypass account restrictions.
    """
    if not 0 < timeout <= 60:
        raise ValueError("Timeout must be 0 < timeout <= 60")
    accounts = set(account_regions)
    if not accounts <= REGIONS.keys():
        raise ValueError("Unknown account region")
    if mode in INDEPENDENT_AREAS:
        raise RegionNotConfigured("Independent area requires verified endpoints")
    if mode == "auto":
        if not order or len(order) != len(set(order)) or any(k not in REGIONS for k in order):
            raise ValueError("Invalid region order")
        candidates = tuple(k for k in order if k in accounts)
    elif mode in REGIONS:
        if mode not in accounts:
            raise RegionNotConfigured("An account for the selected region is required")
        candidates = (mode,)
    else:
        raise ValueError("Unknown region")
    for code in candidates:
        try:
            if await asyncio.wait_for(probe(REGIONS[code]), timeout=timeout) is True:
                return REGIONS[code]
        except (TimeoutError, OSError, ConnectionError):
            continue
    raise NoUsableRegion("No reachable configured region; no login attempted")
