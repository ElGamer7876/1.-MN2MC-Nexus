"""Experimental Mini World Global 1.7.15 inbound compatibility adapter.

The message wire layout used here is *not verified* against Global 1.7.15.
It deliberately parses only the upstream legacy 1.58 envelope and hands
packets to the existing event handlers. Unknown packets are NOT guessed.
"""
from __future__ import annotations

from mn2mc.mini.packet import MiniClientPacket

LEGACY_HEADER = 0x89
MAX_PACKET_BYTES = 65535 + 13

class UnsupportedGlobalPacket(ValueError):
    """Packet cannot be decoded as the provisional shared envelope."""

def decode_client_packet(data: bytes) -> MiniClientPacket:
    """Decode strictly as the legacy envelope, retaining a separate Global hook."""
    if not isinstance(data, bytes):
        raise TypeError("Global client packet must be bytes")
    if len(data) < 13 or len(data) > MAX_PACKET_BYTES:
        raise UnsupportedGlobalPacket("Unexpected packet size")
    if data[0] != LEGACY_HEADER:
        raise UnsupportedGlobalPacket(
            "Unknown Global packet envelope; provide a sanitized sample for adapter research"
        )
    try:
        packet = MiniClientPacket(data)
    except (ValueError, TypeError, OverflowError) as exc:
        raise UnsupportedGlobalPacket("Invalid legacy-compatible Global packet") from exc
    # The upstream parser checks for truncated packets, but does not reject trailing data.
    # Reject it here so unsupported framing is not silently misinterpreted.
    expected = 13 + len(packet.data)
    if len(data) != expected:
        raise UnsupportedGlobalPacket("Unexpected trailing data in Global packet")
    return packet
