import os

import aiohttp

FURIGANA_API_URL = os.environ['FURIGANA_API_URL']

async def furigana(s: str) -> str:
    '''
    >>> await furigana('感じ取れたら手を繋ごう、重なるのは人生のライン and レミリア最高！')
    '感（かん）じ取（と）れたら手（て）を繋（つな）ごう、重（かさ）なるのは人生（じんせい）のライン and レミリア最高（さいこう）！'
    '''
    api_url = FURIGANA_API_URL  # See https://github.com/ayaka14732/furigana-server
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(api_url, data=s) as resp:
                return await resp.text()
        except Exception as e:
            return 'Error: ' + str(e) + '.'
