from typing import Any, Callable, Coroutine

from aiogram.types import Message

from .baidu_translate import translate

import re

def make_handler(f: Callable[[str], str]):
    async def inner(message: Message):
        if message.reply_to_message:
            text = message.reply_to_message.text
            if text:
                text = f(text)
                await message.reply_to_message.reply(text)

        text = message.get_args()
        if text:
            text = f(text)
            await message.reply(text)
    return inner

def make_async_handler(f: Callable[[str], Coroutine[Any, Any, str]]):
    async def inner(message: Message):
        if message.reply_to_message:
            text = message.reply_to_message.text
            if text:
                text = f(text)
                await message.reply_to_message.reply(text)

        text = message.get_args()
        if text:
            text = await f(text)
            await message.reply(text)
    return inner

def make_translate_handler(lang: str):
    async def inner(s: str) -> str:
        return await translate(s, lang)
    return make_async_handler(inner)

def make_transcribe_handler(f: Callable[[str], str], g: Callable[[str], str], w = '(%s)'):
    def inner(text: str):
        def onmatch(match: re.Match):
            s = match[1]
            return s and s + w % g(s)
        res = re.sub(r'[{︷﹛｛](.*?)[}︸﹜｝]', onmatch, text)
        return f(text) if res == text else res
    return make_handler(inner)
