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
    msg: str = str(event.get_message()[0].data)
    await bbdown.finish(msg);




