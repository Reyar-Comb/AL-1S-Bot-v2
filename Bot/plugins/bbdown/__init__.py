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
import shutil
import subprocess
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

                if "-audio" in event.get_message().extract_plain_text():
                    await bbdown.send(f"解析成功！{url}\n选择了仅音频模式喵, 下载进程开始了喵～")
                    result = await run_bbdown(url, audio_only=True, timeout=60)
                else :
                    await bbdown.send(f"解析成功！{url}\n默认下载最高画质喵, 下载进程开始了喵～")
                    result = await run_bbdown(url, audio_only=False, timeout=30)
                await bbdown.finish(f"BBDown输出"{result})
            else:
                await bbdown.send("并非bilibili视频喵")
        else:
            await bbdown.send("并非bilibili视频喵")
    except:
        await asyncio.sleep(0.5)
        if "FinishedException()" in traceback.format_exc(): return
        await bbdown.send("死了喵")
        await bbdown.finish(traceback.format_exc())


async def run_bbdown(url: str, audio_only: bool, timeout: int = 600):
    bbdown_cmd = shutil.which("BBDown")
    if not bbdown_cmd:
        await bbdown.send("BBDown没找到喵")
    proc = await asyncio.create_subprocess_exec(
        bbdown_cmd, # type: ignore
        url,
        "--audio-only" if audio_only else "",
        "--work-dir", "/root/Video")
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
        await bbdown.finish("下载完成喵")
    except asyncio.TimeoutError:
        proc.kill()
        await bbdown.send("下载超时喵")
        return None
    if proc.returncode != 0:
        await bbdown.send("下载失败喵")
        return None
    return stdout