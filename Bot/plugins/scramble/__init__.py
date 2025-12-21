from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from .config import Config
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from .scrambler import get_scramble
from nonebot.params import CommandArg
import time

__plugin_meta__ = PluginMetadata(
    name="Scramble",
    description="Generate scramble sequences for 2x2, 3x3, and 4x4 Rubik's cubes.",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

scramble = on_command("scramble")

@scramble.handle()
async def scramble_handle(event: Event, args: Message = CommandArg()):
    time.sleep(1)
    id = event.get_user_id()
    if not args.extract_plain_text():
        await scramble.finish(MessageSegment.at(id) + " 用法：/scramble <项目>, 例如 /scramble 3")
    elif args.extract_plain_text() not in ["2", "3", "4"]:
        await scramble.finish(MessageSegment.at(id) + " 目前仅支持2/3/4阶魔方喵~")
    else:
        mode = args.extract_plain_text()
        result = get_scramble(mode)
        await scramble.finish(MessageSegment.at(id) + " " + result)
    

