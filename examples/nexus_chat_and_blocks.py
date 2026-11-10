"""Example trusted plugin, only loaded when explicitly configured."""
from mn2mc.nexus.extensions import add_block_mapping, add_chat_hook

def example_chat_hook(message: str, player: object) -> str:
    return message

add_chat_hook(example_chat_hook)
# Enable after verifying IDs for both versions:
# add_block_mapping(mc_id=123, mini_id=456)
