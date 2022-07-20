from dotenv import load_dotenv
load_dotenv()

import os

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ParseMode
from aiogram.utils.exceptions import MessageCantBeDeleted

import ToJyutping
import ToMiddleChinese

from lib.baidu_api_status import BAIDU_API_STATUS
from lib.baidu_translate import translate_to_yue, translate_yue_to_cmn
from lib.furigana import furigana
from lib.greeting import GREETING
from lib.handler import make_async_handler, make_handler, make_translate_handler

BOT_TOKEN = os.environ['BOT_TOKEN']
BAIDU_APP_ID = os.environ['BAIDU_APP_ID']
BAIDU_APP_KEY = os.environ['BAIDU_APP_KEY']

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    await message.reply(GREETING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def register_handler(command, f):
    dp.register_message_handler(f, commands=[command])
    dp.register_edited_message_handler(f, commands=[command])

for command, lang_code, name, status in BAIDU_API_STATUS:
    if status == '1':
        register_handler(command, make_translate_handler(lang_code))

register_handler('yue', make_async_handler(translate_to_yue))
register_handler('cmn', make_async_handler(translate_yue_to_cmn))

register_handler('ja_furi', make_async_handler(furigana))
register_handler('furi', make_async_handler(furigana))

register_handler('och', make_handler(ToMiddleChinese.get_qimyonhmieuzsjyt))
register_handler('och_kyonh', make_handler(ToMiddleChinese.get_kyonh))
register_handler('kyonh', make_handler(ToMiddleChinese.get_kyonh))
register_handler('och_unt', make_handler(ToMiddleChinese.get_unt))
register_handler('unt', make_handler(ToMiddleChinese.get_unt))

register_handler('yue_jyut', make_handler(ToJyutping.get_jyutping))
register_handler('jyut', make_handler(ToJyutping.get_jyutping))

register_handler('yue_ipa', make_handler(ToJyutping.get_ipa))
register_handler('jyut_ipa', make_handler(ToJyutping.get_ipa))

@dp.message_handler(commands=['del'])
async def del_msg(message: Message):
    if message.reply_to_message:
        try:
            await message.reply_to_message.delete()
        except MessageCantBeDeleted:
            pass

@dp.message_handler(commands=['ping'])
async def ping(message: Message):
    await message.reply('pong')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
