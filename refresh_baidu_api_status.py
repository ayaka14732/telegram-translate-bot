import aiohttp
import asyncio
from dotenv import dotenv_values
import hashlib
import random

config = dotenv_values('.env')

BAIDU_APP_ID = config['BAIDU_APP_ID']
BAIDU_APP_KEY = config['BAIDU_APP_KEY']

def md5(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()

async def is_api_working(sentence: str, dest: str, src: str='auto'):
    api_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    salt = str(random.randrange(32768, 67108864))
    payload = {
        'q': sentence,
        'from': src,
        'to': dest,
        'appid': BAIDU_APP_ID,
        'salt': salt,
        'sign': md5(BAIDU_APP_ID + sentence + salt + BAIDU_APP_KEY),
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

sentence = 'Are you OK?'

async def main():
    res = []

    with open('baidu_api_status.csv', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            command, lang_code, *_ = line.rstrip('\n').split(',')
            is_working, _ = await asyncio.gather(
                is_api_working(sentence, lang_code),
                asyncio.sleep(2),
            )
            res.append((command, lang_code, int(is_working)))

    with open('baidu_api_status.csv', 'w', encoding='utf-8') as f:
        print('command,lang_code,status', file=f)
        for command, lang_code, status in res:
            print(command, lang_code, status, sep=',')
            print(command, lang_code, status, file=f, sep=',')

asyncio.run(main())
