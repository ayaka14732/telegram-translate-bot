from typing import Union, Tuple

from aiogram.types import ParseMode

import aiohttp

async def zi(s: str) -> Union[str, Tuple[Union[str, bytes], str]]:
    '''
    The user probably used the wrong bot. Fetch it for the user this time.
    '''
    if not s:
        return 'Meow! I am @suginatransbot. You are probably looking for the official zi.tools bot: /zi@zi_tools_bot'
    api_url = f'http://zu.zi.tools/{s}.png'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as resp:
                if resp.ok:
                    return (await resp.read(), 'I am @suginatransbot, not the official zi.tools bot. Use /zi@zi_tools_bot for full experience.')
                else:
                    return f'I am @suginatransbot, not the official zi.tools bot. Use /zi@zi_tools_bot for full experience.\nInvalid IDS: {s}'
        except Exception as e:
            return 'Error: ' + str(e) + '.'

async def zi_text(s: str) -> Union[str, Tuple[Union[str, bytes], str]]:
    '''
    @zi_tools_bot does not currently support this. It is fair for us to include the functionality.
    '''
    if not s:
        return 'Meow! I am @suginatransbot. Enter `/zi_text (IDS)` to get a character in ASCII art. You might want to check out the official zi.tools bot too: /zi@zi_tools_bot'
    api_url = f'http://zu.zi.tools/{s}.txt'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as resp:
                if resp.ok:
                    return (f'```\n{await resp.text()}\n```', ParseMode.MARKDOWN)
                else:
                    return f'Invalid IDS: {s}'
        except Exception as e:
            return 'Error: ' + str(e) + '.'
