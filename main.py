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
from lib.zi import zi
from lib.greeting import GREETING
from lib.handler import make_async_handler, make_handler, make_translate_handler, make_transcribe_handler

BOT_TOKEN = os.environ['BOT_TOKEN']
BAIDU_APP_ID = os.environ['BAIDU_APP_ID']
BAIDU_APP_KEY = os.environ['BAIDU_APP_KEY']

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    await message.reply(GREETING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def register_handler(commands, f):
    dp.register_message_handler(f, commands=commands)
    dp.register_edited_message_handler(f, commands=commands)

for command, lang_code, name, status in BAIDU_API_STATUS:
    if status == '1':
        register_handler([command], make_translate_handler(lang_code))

register_handler(['yue'], make_async_handler(translate_to_yue))
register_handler(['cmn'], make_async_handler(translate_yue_to_cmn))
register_handler(['ja_furi', 'furi'], make_async_handler(furigana))

register_handler(['och', 'lzh'], make_transcribe_handler(ToMiddleChinese.get_pos, ToMiddleChinese.get_pos_text, '（%s）'))
register_handler(['och_text', 'lzh_text'], make_handler(ToMiddleChinese.get_pos_text))
register_handler(['och_tupa', 'lzh_tupa', 'tupa'], make_transcribe_handler(ToMiddleChinese.get_tupa, ToMiddleChinese.get_tupa_text))
register_handler(['och_tupa_text', 'lzh_tupa_text', 'tupa_text'], make_handler(ToMiddleChinese.get_tupa_text))
register_handler(['och_kyonh', 'lzh_kyonh', 'kyonh'], make_transcribe_handler(ToMiddleChinese.get_kyonh, ToMiddleChinese.get_kyonh_text))
register_handler(['och_kyonh_text', 'lzh_kyonh_text', 'kyonh_text'], make_handler(ToMiddleChinese.get_kyonh_text))
register_handler(['och_unt', 'lzh_unt', 'unt'], make_transcribe_handler(ToMiddleChinese.get_unt, ToMiddleChinese.get_unt_text, '[%s]'))
register_handler(['och_unt_text', 'lzh_unt_text', 'unt_text'], make_handler(ToMiddleChinese.get_unt_text))

register_handler(['yue_jyut', 'jyut'], make_transcribe_handler(ToJyutping.get_jyutping, ToJyutping.get_jyutping_text))
register_handler(['yue_text', 'jyut_text'], make_handler(ToJyutping.get_jyutping_text))
register_handler(['yue_ipa', 'jyut_ipa'], make_transcribe_handler(ToJyutping.get_ipa, ToJyutping.get_ipa_text, '[%s]'))
register_handler(['yue_ipa_text', 'jyut_ipa_text'], make_handler(ToJyutping.get_ipa_text))

register_handler(['zi'], make_handler(zi))

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
