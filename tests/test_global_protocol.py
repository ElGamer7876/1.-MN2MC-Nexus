"""Offline packet-envelope experiments only; not a Global compatibility proof."""
import pytest
from mn2mc.mini.packet import MiniClientPacket
from mn2mc.nexus.global_protocol import decode_client_packet, UnsupportedGlobalPacket

def test_legacy_compatible_envelope_roundtrip():
    original = MiniClientPacket(123, 13, b"test", 456).encode()
    decoded = decode_client_packet(original)
    assert decoded.uin == 123
    assert decoded.touin == 456
    assert decoded.msgcode == 13
    assert decoded.data == b"test"

@pytest.mark.parametrize("raw", [b"", b"X"*12, b"\x00"+b"\x00"*12, b"\x89"+b"\x00"*12+b"x"])
def test_rejects_unsupported_packets(raw):
    with pytest.raises(UnsupportedGlobalPacket):
        decode_client_packet(raw)

def test_does_not_silently_accept_trailing_bytes():
    raw = MiniClientPacket(1, 2, b"x", 3).encode() + b"ignored"
    with pytest.raises(UnsupportedGlobalPacket):
        decode_client_packet(raw)
