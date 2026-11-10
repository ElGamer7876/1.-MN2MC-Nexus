"""Trusted optional Mini World outbound chat and numeric block mapping hooks."""
from collections.abc import Callable
from loguru import logger

_chat_hooks: list[Callable[[str, object], str | None]] = []
_mc_to_mini: dict[int, int] = {}
_mini_to_mc: dict[int, int] = {}

def add_chat_hook(hook: Callable[[str, object], str | None]) -> None:
    if not callable(hook):
        raise TypeError("Chat hook must be callable")
    if hook not in _chat_hooks:
        _chat_hooks.append(hook)

def transform_chat(message: str, player: object) -> str | None:
    for hook in tuple(_chat_hooks):
        try:
            change = hook(message, player)
            if change is None:
                return None
            if not isinstance(change, str):
                raise TypeError("Chat hook must return str or None")
            message = change
        except Exception:
            logger.exception("Chat extension failed; preserving previous message")
    return message

def add_block_mapping(mc_id: int, mini_id: int) -> None:
    if type(mc_id) is not int or type(mini_id) is not int or min(mc_id, mini_id) < 0:
        raise ValueError("Block IDs must be nonnegative integers")
    previous_mini = _mc_to_mini.pop(mc_id, None)
    if previous_mini is not None:
        _mini_to_mc.pop(previous_mini, None)
    previous_mc = _mini_to_mc.pop(mini_id, None)
    if previous_mc is not None:
        _mc_to_mini.pop(previous_mc, None)
    _mc_to_mini[mc_id] = mini_id
    _mini_to_mc[mini_id] = mc_id

def resolve_mc_block(mc_id: int) -> int | None:
    return _mc_to_mini.get(mc_id)

def resolve_mini_block(mini_id: int) -> int | None:
    return _mini_to_mc.get(mini_id)

def reset_extensions() -> None:
    _chat_hooks.clear()
    _mc_to_mini.clear()
    _mini_to_mc.clear()
