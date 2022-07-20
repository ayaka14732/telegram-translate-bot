from typing import Any, Callable, Coroutine

from aiogram.types import Message

from .baidu_translate import translate

def make_handler(f: Callable[[str], str]):
    async def inner(message: Message):
        if message.reply_to_message:
            text = message.reply_to_message.text
        else:
            text = message.get_args()

        if text:
            text = f(text)
            await message.reply(text)
    return inner

def make_async_handler(f: Callable[[str], Coroutine[Any, Any, str]]):
    async def inner(message: Message):
        if message.reply_to_message:
            text = message.reply_to_message.text
        else:
            text = message.get_args()

        if text:
            text = await f(text)
            await message.reply(text)
    return inner

def _make_translator(lang: str) -> Callable[[str], Coroutine[Any, Any, str]]:
    async def f(s: str) -> str:
        return await translate(s, lang)
    return f

def make_translate_handler(lang: str):
    return make_async_handler(_make_translator(lang))
