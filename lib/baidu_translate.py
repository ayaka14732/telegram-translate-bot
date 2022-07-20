import aiohttp
from opencc import OpenCC
import os
import random

from .md5 import md5

_BAIDU_APP_ID = os.environ['BAIDU_APP_ID']
_BAIDU_APP_KEY = os.environ['BAIDU_APP_KEY']

_simp2trad = OpenCC('s2hk').convert

def format_error_code(error_code: str) -> str:
    default_descr = 'Error: error code ' + error_code + '. Please contact the manager.'
    return {
        '54003': 'Error: Access frequency is limited. Please reduce your calling frequency.',
        '54004': 'Error: The account balance is insufficient. Please contact the manager to recharge the account.',
        '54005': 'Error: Long requests are too frequent. Please reduce the sending frequency of long queries and try again in 3 seconds.',
        '58001': 'Error: Support for this language has been temporarily cancelled.',
        '58002': 'Error: The service is currently down. Please contact the manager to start the service.',
    }.get(error_code, default_descr)

async def is_api_working(sentence: str, dest: str, src: str='auto') -> bool:
    api_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    salt = str(random.randrange(32768, 67108864))
    payload = {
        'q': sentence,
        'from': src,
        'to': dest,
        'appid': _BAIDU_APP_ID,
        'salt': salt,
        'sign': md5(_BAIDU_APP_ID + sentence + salt + _BAIDU_APP_KEY),
    }

    while True:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, data=payload) as resp:
                    obj = await resp.json()
                    if 'error_code' not in obj:
                        return True
                    if obj['error_code'] == '58001':
                        return False
            except Exception:
                pass

async def translate(sentence: str, dest: str, src: str='auto') -> str:
    api_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    salt = str(random.randrange(32768, 67108864))
    payload = {
        'q': sentence,
        'from': src,
        'to': dest,
        'appid': _BAIDU_APP_ID,
        'salt': salt,
        'sign': md5(_BAIDU_APP_ID + sentence + salt + _BAIDU_APP_KEY),
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(api_url, data=payload) as resp:
                obj = await resp.json()
                if 'error_code' in obj:
                    return format_error_code(obj['error_code'])
                else:
                    text = '\n'.join(x['dst'] for x in obj['trans_result'])
                    return text
        except Exception as e:
            return 'Error: ' + str(e) + '.'

async def translate_to_yue(s: str) -> str:
    s = await translate(s, 'yue')
    s = _simp2trad(s)
    s = s.replace('系', '係')  # 係 is more commonly used in Cantonese
    return s

async def translate_yue_to_cmn(s: str) -> str:
    s = await translate(s, 'cht', src='yue')
    return s
