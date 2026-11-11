"""Edition profiles. The Global legacy-codec experiment is not verified crossplay."""
from __future__ import annotations
from dataclasses import dataclass

CHINA_VERSION = "1.58.0"
CHINA_CLIENT_VERSION_CODE = 80384
GLOBAL_VERSION = "1.7.15"

@dataclass(frozen=True)
class EditionPlan:
    edition: str
    mini_version: str
    port: int
    client_version_code: int | None
    status: str

def plan_edition(edition: str, global_port: int = 11155, china_port: int = 11156,
                 global_client_version_code: int | None = None) -> EditionPlan:
    if edition not in {"global", "china"}:
        raise ValueError("Unknown game edition")
    if any(type(p) is not int or not 1 <= p <= 65535 for p in (global_port, china_port)):
        raise ValueError("Ports must be between 1 and 65535")
    if global_client_version_code is not None and (
        type(global_client_version_code) is not int
        or not 1 <= global_client_version_code <= 4294967295
    ):
        raise ValueError("Global client version code must be a positive 32-bit integer")
    if edition == "china":
        return EditionPlan("china", CHINA_VERSION, china_port,
                           CHINA_CLIENT_VERSION_CODE, "upstream-legacy")
    return EditionPlan("global", GLOBAL_VERSION, global_port,
                       global_client_version_code, "experimental-unverified-codec")

def validate_dual_ports(global_port: int, china_port: int) -> None:
    if global_port == china_port:
        raise ValueError("Both editions must use different UDP ports")

def apply_edition(plan: EditionPlan, config_module) -> None:
    """Configure process-local edition BEFORE importing packet and room handlers."""
    import mn2mc.mini as mini

    mini.version = plan.mini_version
    # Do not send the Chinese client version code in the Global profile.
    mini.cltversion = plan.client_version_code if plan.client_version_code is not None else 0
    config_module.mini.server.port = plan.port
    if plan.edition == "global":
        # The original room/auth implementation uses Chinese mini1.cn endpoints.
        # It must never be called from the experimental Global edition.
        config_module.mini.server.host_to_room_server = False
