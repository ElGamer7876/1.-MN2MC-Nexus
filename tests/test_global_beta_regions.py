"""Offline verification of XML-derived candidates and opt-in beta policy."""
import asyncio
import pytest
from mn2mc.nexus.regions import REGIONS, select_region, RegionNotConfigured

def run(awaitable):
    return asyncio.run(awaitable)

@pytest.mark.parametrize("region,suffix", [
    ("usz", "usz"), ("hkz", "hkz"), ("jpz", "jpz"),
    ("brz", "brz"), ("ruz", "ruz"), ("gerz", "gerz"),
    ("vnz", "vnz"), ("thz", "thz"), ("sgpz", "sgpz"),
    ("inaz", "inaz"), ("twz", "twz"),
    ("ussz", "us_sz"), ("brnz", "brnz"),
])
def test_region_candidate_host_facts(region, suffix):
    entry = REGIONS[region]
    assert entry.room_host == f"openroom-{suffix}.miniworldgame.com"
    assert entry.auth_host == f"acchm-{suffix}.miniworldgame.com"
    assert entry.room_port == 8080
    assert entry.auth_port == 4000
    assert entry.source_file
    assert entry.verified_login is False

def test_global_hosts_are_not_authenticated_endpoints():
    assert not any(item.verified_login for item in REGIONS.values())
    assert "global" not in REGIONS
    assert REGIONS["overseas"].source_file == "serverlist.xml"

def test_beta_new_region_requires_matching_account():
    seen = []
    async def probe(region):
        seen.append(region.code)
        return region.code == "brz"
    result = run(select_region(probe, {"brz"}, "auto"))
    assert result.code == "brz" and seen == ["brz"]
    with pytest.raises(RegionNotConfigured):
        run(select_region(probe, {"usz"}, "brz"))
    assert seen == ["brz"]

def test_region_label_is_not_account_code():
    async def probe(_region):
        raise AssertionError("Should not probe an unknown code")
    with pytest.raises(RegionNotConfigured):
        run(select_region(probe, {"brz"}, "brazil"))
