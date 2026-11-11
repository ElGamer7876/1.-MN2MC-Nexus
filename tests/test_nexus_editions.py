"""Offline tests: no game accounts or network connections required."""
import pytest
from mn2mc.nexus.editions import plan_edition, apply_edition, validate_dual_ports
from mn2mc.nexus.launcher import get_plans
from mn2mc.config import RuntimeConfig

def test_global_is_default():
    config = RuntimeConfig()
    assert config.mode == "global"
    assert [p.edition for p in get_plans(config.mode, config)] == ["global"]

def test_both_run_on_different_ports():
    plans = get_plans("both", RuntimeConfig())
    assert [(p.edition, p.port) for p in plans] == [("global",11155),("china",11156)]

def test_do_not_forge_global_protocol_version():
    p = plan_edition("global")
    assert p.client_version_code is None
    assert p.status == "experimental-unverified-codec"

def test_china_upstream_is_preserved():
    p = plan_edition("china")
    assert (p.mini_version,p.client_version_code) == ("1.58.0",80384)

def test_bad_port_and_collision_rejected():
    with pytest.raises(ValueError):
        validate_dual_ports(11155,11155)
    with pytest.raises(ValueError):
        get_plans("both", RuntimeConfig(global_port=11155,china_port=11155))
    with pytest.raises(ValueError):
        plan_edition("unknown")
    with pytest.raises(ValueError):
        get_plans("global",RuntimeConfig(),port_override=0)

def test_global_does_not_use_chinese_room_host():
    import mn2mc.config as cfg
    import mn2mc.mini as mini
    orig = (cfg.config.mini.server.port,cfg.config.mini.server.host_to_room_server,mini.version,mini.cltversion)
    try:
        cfg.config.mini.server.host_to_room_server = True
        apply_edition(plan_edition("global"),cfg)
        assert cfg.config.mini.server.host_to_room_server is False
        assert mini.version == "1.7.15"
        assert mini.cltversion == 0
    finally:
        cfg.config.mini.server.port,cfg.config.mini.server.host_to_room_server,mini.version,mini.cltversion = orig

def test_china_keeps_room_mode():
    import mn2mc.config as cfg
    import mn2mc.mini as mini
    orig = (cfg.config.mini.server.port,cfg.config.mini.server.host_to_room_server,mini.version,mini.cltversion)
    try:
        cfg.config.mini.server.host_to_room_server = True
        apply_edition(plan_edition("china"),cfg)
        assert cfg.config.mini.server.host_to_room_server is True
        assert mini.version == "1.58.0"
        assert mini.cltversion == 80384
    finally:
        cfg.config.mini.server.port,cfg.config.mini.server.host_to_room_server,mini.version,mini.cltversion = orig
