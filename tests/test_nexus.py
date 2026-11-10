"""Offline unit tests; no network connection or accounts required."""
import asyncio
import pytest
from mn2mc.nexus.regions import NoUsableRegion, RegionNotConfigured, select_region
from mn2mc.nexus.rooms import RoomPool
from mn2mc.nexus.extensions import (
    add_chat_hook, add_block_mapping, reset_extensions,
    transform_chat, resolve_mc_block, resolve_mini_block,
)

def run(coro):
    return asyncio.run(coro)

def test_failover_only_regions_with_account():
    checked = []
    async def probe(region):
        checked.append(region.code)
        return region.code == "usz"
    assert run(select_region(probe, {"overseas", "usz"})).code == "usz"
    assert checked == ["overseas", "usz"]

def test_cannot_enter_region_without_account():
    async def forbidden(region):
        raise AssertionError("no probe expected")
    with pytest.raises(RegionNotConfigured):
        run(select_region(forbidden, {"usz"}, "hkz"))
    with pytest.raises(NoUsableRegion):
        run(select_region(forbidden, set()))
    with pytest.raises(RegionNotConfigured):
        run(select_region(forbidden, {"usz"}, "brazil"))

def test_new_room_on_full_capacity():
    async def scenario():
        calls = []
        async def creator(region, alias, capacity):
            calls.append((region.code, alias, capacity))
            return "room-2"
        pool = RoomPool({"usz": ["alt1", "alt2"]}, auto_expand=True, create_room=creator)
        pool.attach_room("usz", "alt1", "room-1")
        assert pool.max_rooms("usz") == 2
        assert pool.max_capacity("usz") == 80
        assert await pool.update_occupancy("room-1", 39) is None
        result = await pool.update_occupancy("room-1", 40)
        assert result.room_id == "room-2"
        assert result.account_alias == "alt2"
        assert calls == [("usz", "alt2", 40)]
        assert await pool.update_occupancy("room-1", 40) is None
    run(scenario())

def test_no_automatic_creation_without_verified_provider():
    async def scenario():
        pool = RoomPool({"hkz": ["host1", "host2"]}, auto_expand=True)
        pool.attach_room("hkz", "host1", "one")
        assert await pool.update_occupancy("one", 40) is None
        assert len(pool.rooms) == 1
    run(scenario())

def test_chat_and_block_overrides():
    reset_extensions()
    add_chat_hook(lambda message, player: "PREFIX " + message)
    assert transform_chat("hi", object()) == "PREFIX hi"
    add_block_mapping(1234, 5678)
    assert resolve_mc_block(1234) == 5678
    assert resolve_mini_block(5678) == 1234
    reset_extensions()
