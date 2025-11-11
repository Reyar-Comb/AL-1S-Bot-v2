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
        data = seg.data["data"]
        
        if isinstance(data, str):
            if "哔哩哔哩" in data:
                data = data.replace('\n', '')
                data = data.replace('\\/', '/')
                parsed = json.loads(data)
                url = parsed['meta']['detail_1']['qqdocurl']
                await bbdown.send(f"下载链接喵：{url}")
            else:
                await bbdown.send("这不是哔哩哔哩小程序喵")
        else:
            await bbdown.send("这不是哔哩哔哩小程序喵")
    except:
        await asyncio.sleep(0.5)
        await bbdown.send("死了喵")
        await bbdown.finish(traceback.format_exc())


