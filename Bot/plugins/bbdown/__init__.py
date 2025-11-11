from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from nonebot import on_command
import requests # type: ignore
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
        await bbdown.finish("并非reply喵")
    reply = event.reply
    reply_msg = reply.message
    rich_text = reply_msg.to_rich_text()
    await bbdown.send(reply_msg)
    await bbdown.finish("提取到了:\n" + rich_text)


