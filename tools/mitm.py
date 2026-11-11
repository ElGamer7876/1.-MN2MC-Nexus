import json
import os

from mitmproxy import http


def _get_china_port() -> int:
    """China listener defaults to upstream UDP 11155; override if needed."""
    port = int(os.getenv("MN2MC_CHINA_PORT", "11155"))
    if not 1 <= port <= 65535:
        raise ValueError("MN2MC_CHINA_PORT out of range")
    return port


def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url == "http://cs-gsmgr.mini1.cn/v2/room/get":
        data = {
            "code": 0,
            "msg": "found",
            "aid": "10213705870553",
            "roomid": "MN2MC-MitmMode",
            "ip": "127.0.0.1",
            "port": _get_china_port(),
            "room_cap": 1,
            "player_num": 0,
            "mod_url": "",
            "room_mods": "",
            "room_ui_libs": "",
            "room_ver": "1.58.0",
            "room_name": "MN2MC",
            "room_audio_config": '{"editorSceneSwitch":0,"worldtype":4}',
            "room_translate": "",
            "czb_uuid": "",
            "uin": 1000,
            "nick_name": "ReYueY1ng",
            "is_cloud": False,
            "passwd_md5": "",
            "share_version": "1772094792",
            "team_id": 0,
            "public_type": 0,
            "can_trace": 0,
            "personal": 0,
            "teams": [],
            "room_from": "",
            "not_follow": False,
        }
        flow.response = http.Response.make(
            200,  # (optional) status code
            json.dumps(data),
            {"Content-Type": "application/json; charset=utf-8"},  # (optional) headers
        )
