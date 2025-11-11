from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from nonebot import on_command
import requests # type: ignore
from time import time
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
        await time.sleep(1)
        await bbdown.finish("并非reply喵")
    reply = event.reply
    reply_msg = reply.message
    url = ""
    print(reply_msg[0].data)
    await bbdown.finish("功能维护中喵")


