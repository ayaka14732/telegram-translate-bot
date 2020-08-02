# basic functions

import logging
import os

# call Baidu translate API

import hashlib  # for MD5
import httpx
import random  # for generating salt

# call local libraries

from opencc import OpenCC  # for Simplified Chinese to Traditional Chinese
import ToJyutping  # for Cantonese transcription
import ToMiddleChinese  # for Middle Chinese transcription

# Telegram bot

from aiogram import Bot, types, md, Dispatcher, executor
from aiogram.utils.executor import start_webhook

# secrets

BOT_TOKEN = os.environ['BOT_TOKEN']
WEBHOOK_HOST = os.environ['WEBHOOK_HOST']  # example: 'https://blooming-savannah-04752.herokuapp.com'
WEBHOOK_PATH = os.environ.get('WEBHOOK_PATH', '/')  # example: '/path/to/webhook/'

BAIDU_APP_ID = os.environ['BAIDU_APP_ID']
BAIDU_APP_KEY = os.environ['BAIDU_APP_KEY']

# configuration

WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

GREETINGS = '''Meow! I am the translator bot. I can help you to do the following things.

**Translate to a language:**

`/de` Translate to German
`/en` Translate to English
`/es` Translate to Spanish
`/fr` Translate to French
`/ja` Translate to Japanese
`/ko` Translate to Korean
`/pt` Translate to Portuguese
`/ru` Translate to Russian
`/th` Translate to Thai
`/zh` Translate to Chinese
`/cmn` Translate to Mandarin (from Cantonese)
`/yue` Translate to Cantonese

**Transcription:**

`/och` Text labeling by Middle Chinese
`/yue_jyut` Text labeling by Cantonese pronunciation (Jyutping)
`/yue_ipa` Text labeling by Cantonese pronunciation (IPA)

**Others:**

`/ping` Test the server connection

If you find me not working properly, you can [report an issue](https://github.com/ayaka14732/trans) to my developers.'''

# Baidu translate

def md5(s):
	return hashlib.md5(s.encode('utf-8')).hexdigest()

async def translate(s, dest, src='auto'):
	api_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
	salt = str(random.randrange(32768, 67108864))
	payload = \
		{ 'q': s
		, 'from': src
		, 'to': dest
		, 'appid': BAIDU_APP_ID
		, 'salt': salt
		, 'sign': md5(BAIDU_APP_ID + s + salt + BAIDU_APP_KEY)
		}
	try:
		async with httpx.AsyncClient() as client:
			r = await client.post(api_url, data=payload, timeout=300.0)  # Wait for 5 min
		obj = r.json()
		if 'error_code' in obj:
			error_code = obj['error_code']
			default_descr = 'Error: error code ' + error_code + '. Please contact the manager.'
			return \
				{ '54003': 'Error: Access frequency is limited. Please reduce your calling frequency.'
				, '54004': 'Error: The account balance is insufficient. Please contact the manager to recharge the account.'
				, '54005': 'Error: Long requests are too frequent. Please reduce the sending frequency of long queries and try again in 3 seconds.'
				, '58002': 'Error: The service is currently down. Please contact the manager to start the service.'
				}.get(error_code, default_descr)
		else:
			text = '\n'.join(x['dst'] for x in obj['trans_result'])
			return text
	except Exception as e:
		return 'Error: ' + str(e) + '.'

# initialize

logging.basicConfig(level=logging.INFO)

traditionalize = OpenCC('s2hk').convert

# initialize bot

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# handle help command

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	await message.answer(GREETINGS, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)

# register command handler

def register_handler(command, f):
	dp.register_message_handler(f, commands=[command])
	dp.register_edited_message_handler(f, commands=[command])

# register Baidu translator

def create_translator(lang):
	async def f(message: types.Message):
		text = message.get_args()
		if text:
			text = await translate(text, lang)
			await message.reply(text)
	return f

register_handler('nl', create_translator('nl'))
register_handler('ms', create_translator('may'))
register_handler('th', create_translator('th'))
register_handler('es', create_translator('spa'))
register_handler('sr', create_translator('srp'))
register_handler('pt', create_translator('pt'))
register_handler('la', create_translator('lat'))
register_handler('my', create_translator('bur'))
register_handler('fr', create_translator('fra'))
register_handler('pl', create_translator('pl'))
register_handler('ar', create_translator('ara'))
register_handler('et', create_translator('est'))
register_handler('ja', create_translator('jp'))
register_handler('zh', create_translator('cht'))
register_handler('en', create_translator('en'))
register_handler('de', create_translator('de'))
register_handler('ko', create_translator('kor'))
register_handler('ru', create_translator('ru'))
register_handler('vi', create_translator('vie'))
register_handler('ga', create_translator('gle'))
register_handler('uz', create_translator('uzb'))
register_handler('ka', create_translator('geo'))
register_handler('lzh', create_translator('wyw'))

# special treatment for some Baidu translate commands

@dp.message_handler(commands=['yue'])
@dp.edited_message_handler(commands=['yue'])
async def translate_yue(message: types.Message):
	text = message.get_args()
	if text:
		text = await translate(text, 'yue')
		text = traditionalize(text)
		text = text.replace('系', '係')  # 係 is more commonly used in Cantonese
		await message.reply(text)

@dp.message_handler(commands=['cmn'])
@dp.edited_message_handler(commands=['cmn'])
async def translate_cmn(message: types.Message):
	text = message.get_args()
	if text:
		text = await translate(text, 'cht', src='yue')
		await message.reply(text)

# register translate functions in local libraries

def create_transformer(trans):
	async def f(message: types.Message):
		text = message.get_args()
		if text:
			text = trans(text)
			await message.reply(text)
	return f

register_handler('och', create_transformer(ToMiddleChinese.get_qimyonhmieuzsjyt))
register_handler('och_kuxyonh', create_transformer(ToMiddleChinese.get_kuxyonh))
register_handler('och_unt', create_transformer(ToMiddleChinese.get_unt))
register_handler('yue_jyut', create_transformer(ToJyutping.get_jyutping))
register_handler('yue_ipa', create_transformer(ToJyutping.get_ipa))

@dp.message_handler(commands=['ping'])
@dp.edited_message_handler(commands=['ping'])
async def ping(message: types.Message):
	await message.reply('pong')

# start the bot

async def on_startup(dp):
	await bot.set_webhook(WEBHOOK_URL)

if __name__ == '__main__':
	start_webhook \
		( dispatcher=dp
		, webhook_path=WEBHOOK_PATH
		, on_startup=on_startup
		, host=WEBAPP_HOST
		, port=WEBAPP_PORT
		)
