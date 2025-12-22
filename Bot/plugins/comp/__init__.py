from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from .config import Config
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from .get_comp import get_comp
import time
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
    result += "戳这里看更多哦：\nhttps://cubing.com/competition"
    await comp.finish(result)