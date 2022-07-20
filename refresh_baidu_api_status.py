import asyncio

from lib.baidu_translate import is_api_working

interval = 2
sentence = '天気がいいから、散歩しましょう'

async def main():
    res = []

    with open('lib/baidu_api_status.csv', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            command, lang_code, name, _ = line.rstrip('\n').split(',')
            is_working, _ = await asyncio.gather(
                is_api_working(sentence, lang_code),
                asyncio.sleep(interval),  # avoid 429
            )
            status = int(is_working)
            print(command, lang_code, name, status, sep=',')
            res.append((command, lang_code, name, status))

    with open('lib/baidu_api_status.csv', 'w', encoding='utf-8') as f:
        print('command,lang_code,name,status', file=f)
        for command, lang_code, name, status in res:
            print(command, lang_code, name, status, sep=',', file=f)

asyncio.run(main())
