"""Offline tests with synthetic XML. No game assets are bundled."""
from pathlib import Path
import pytest
from scripts.inspect_global_xml import compare_catalog, inspect_xml

def test_valid_synthetic_usz_xml(tmp_path: Path):
    file = tmp_path / "serverlist_usz.xml"
    file.write_text("""<Config>
        <RoomHostHttp url="openroom-usz.miniworldgame.com" port="8080" />
        <Websocket url="http://acchm-usz.miniworldgame.com:4000/" />
    </Config>""")
    got = inspect_xml(file)
    assert got == {"room_host": "openroom-usz.miniworldgame.com",
                   "room_port": 8080, "auth_host": "acchm-usz.miniworldgame.com", "auth_port": 4000}
    rows = compare_catalog(tmp_path)
    assert next(row for row in rows if row["region"] == "usz")["status"] == "match"
    assert next(row for row in rows if row["region"] == "jpz")["status"] == "missing"

def test_differing_local_client_xml_is_reported(tmp_path: Path):
    f = tmp_path / "serverlist_brz.xml"
    f.write_text('<Config><RoomHostHttp url="openroom-br.miniworldgame.com" port="8080" />'
                 '<Websocket url="http://acchm-br.miniworldgame.com:4000/" /></Config>')
    entry = next(x for x in compare_catalog(tmp_path) if x["region"] == "brz")
    assert entry["status"] == "mismatch"

@pytest.mark.parametrize("xml", [
    '<Wrong />',
    '<Config><RoomHostHttp url="other.example.com" port="8080" />'
    '<Websocket url="http://acchm-usz.miniworldgame.com:4000/" /></Config>',
    '<Config><RoomHostHttp url="openroom-usz.miniworldgame.com" port="8080" /></Config>',
])
def test_rejects_bad_or_unrelated_metadata(tmp_path: Path, xml):
    path = tmp_path / "serverlist.xml"
    path.write_text(xml)
    with pytest.raises(ValueError):
        inspect_xml(path)
