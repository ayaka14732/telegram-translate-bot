import aiohttp

async def furigana(s: str) -> str:
    '''
    >>> await furigana('感じ取れたら手を繋ごう、重なるのは人生のライン and レミリア最高！')
    '感（かん）じ取（と）れたら手（て）を繋（つな）ごう、重（かさ）なるのは人生（じんせい）のライン and レミリア最高（さいこう）！'
    '''
    api_url = 'https://ayaka-apps.shn.hk/furigana/'  # See https://github.com/ayaka14732/kuroshiro
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(api_url, data=s) as resp:
                return await resp.text()
        except Exception as e:
            return 'Error: ' + str(e) + '.'
