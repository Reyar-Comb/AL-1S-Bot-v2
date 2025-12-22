from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from .config import Config
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from .get_comp import get_comp
from time import time
__plugin_meta__ = PluginMetadata(
    name="Comp",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

comp = on_command("comp")

@comp.handle()
async def comp_handle():
    time.sleep(1)
    result = get_comp()
    await comp.finish(result)