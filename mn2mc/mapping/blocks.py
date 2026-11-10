from mn2mc.data.loader import load_blocks
from mn2mc.mapping.base import BidirectionalMapping
from mn2mc.nexus.extensions import resolve_mc_block, resolve_mini_block

# MC id: Mini id
_mapping = BidirectionalMapping(load_blocks(), mc_default=470, mini_default=9)
mc_to_mini_mapping: dict[int, int] = _mapping.forward
mini_to_mc_mapping: dict[int, int] = _mapping.reverse


def mc_to_mini(id: int) -> int:
    custom = resolve_mc_block(id)
    return custom if custom is not None else _mapping.mc_to_mini(id)


def mini_to_mc(id: int) -> int:
    custom = resolve_mini_block(id)
    return custom if custom is not None else _mapping.mini_to_mc(id)
