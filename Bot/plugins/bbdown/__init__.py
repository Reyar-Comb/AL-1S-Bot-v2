from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from nonebot import on_command
import requests # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event

__plugin_meta__ = PluginMetadata(
    name="bbdown",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

bbdown = on_command("dl")

@bbdown.handle()
async def bbdown_handle(event: Event):
    msgs: Message = Message()
    for i in event.get_message():
        msgs += i
    await bbdown.finish(str(msgs))


