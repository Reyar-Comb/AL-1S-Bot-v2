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
import os
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
                name = parsed['meta']['detail_1']['desc']

                if "-audio" in event.get_message().extract_plain_text():
                    await bbdown.send(f"解析成功！{url}\n选择了仅音频模式喵, 下载进程开始了喵～")
                    url = await redirect(url)
                    result = await run_bbdown(url, audio_only=True, timeout=60)
                else :
                    await bbdown.send(f"解析成功！{url}\n默认下载最高画质喵, 下载进程开始了喵～")
                    url = await redirect(url)
                    result = await run_bbdown(url, audio_only=False, timeout=30)

                msg = f"BBDown输出{result}"
                if "None" in msg:
                    await bbdown.send("下载成功喵, 正在尝试发送喵")

                    path = await find(name, audio_only=("-audio" in event.get_message().extract_plain_text()))
                    if path == "err":
                        await bbdown.send("下载失败喵")
                        return
                    seg = MessageSegment.video(f"file://{path}")
                    id = event.get_user_id()
                    await bbdown.send(Message(seg))
                    delete(path)
                    await bbdown.finish(MessageSegment.at(id) + " 已发送喵")

                else:
                    await bbdown.finish(f"BBDown输出{result}")
                
                    

            else:
                await bbdown.send("并非bilibili视频喵")
        else:
            await bbdown.send("并非bilibili视频喵")
    except:
        await asyncio.sleep(0.5)
        if "FinishedException()" in traceback.format_exc(): return
        elif "WebSocket call api" in traceback.format_exc(): return
        await bbdown.send("死了喵")
        await bbdown.finish(traceback.format_exc())


async def run_bbdown(url: str, audio_only: bool, timeout: int = 600):
    bbdown_cmd = shutil.which("BBDown")
    if not bbdown_cmd:
        await bbdown.send("BBDown没找到喵")
    if audio_only:
        proc = await asyncio.create_subprocess_exec(
            bbdown_cmd, # type: ignore
            url,
            "--audio-only",
            "--work-dir", "/root/Video")
    else:
        proc = await asyncio.create_subprocess_exec(
            bbdown_cmd, # type: ignore
            url,
            "--work-dir", "/root/Video")
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
    except asyncio.TimeoutError:
        proc.kill()
        await bbdown.send("下载超时喵")
        return None
    if proc.returncode != 0:
        await bbdown.send("下载失败喵")
        return None
    return stdout

async def redirect(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AL-1S-Bot/1.0)"
    }
    try:
        response = await asyncio.to_thread(
            lambda: requests.get(url, allow_redirects=True, timeout=10, headers=headers)
        )
        final = getattr(response, 'url', url) or url
        return final
    except Exception as e:
        logging.error(f"Redirect error: {e}")
        await bbdown.send("展开短链失败喵")
        return url

async def find(name: str, audio_only: bool) -> str:
    for root, dirs, files in os.walk("/root/Video"):
        for file in files:
            if name in file:
                return os.path.join(root, file)
    return "err"

def delete(url: str):
    try:
        os.remove(url)
    except Exception as e:
        logging.error(f"Delete error: {e}")