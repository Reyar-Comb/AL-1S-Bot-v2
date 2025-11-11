from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from nonebot import on_command
import requests # type: ignore
import asyncio
import time
import logging
import traceback
import json
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event, MessageEvent


__plugin_meta__ = PluginMetadata(
    name="bbdown",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

bbdown = on_command("dl")

@bbdown.handle()
async def bbdown_handle(event: MessageEvent):
    if not event.reply:
        await asyncio.sleep(0.5)
        await bbdown.finish("并非reply喵")
    reply = event.reply
    reply_msg = reply.message
    url = ""
    try:
        await asyncio.sleep(0.5)
        seg = reply_msg[0]
        data = seg.data
        parsed = json.loads(json.dumps(data))
        print(parsed)
        url = (parsed.get("meta", {}).get("detail_1", {}).get("qqdocurl", ""))
        await bbdown.send(f"下载链接喵：{url}")
    except:
        await asyncio.sleep(0.5)
        await bbdown.send("死了喵")
        await bbdown.finish(traceback.format_exc())


