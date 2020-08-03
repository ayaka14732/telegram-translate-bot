# basic functions

import logging
import os

# call Baidu translate API

import aiohttp
import hashlib  # for MD5
import random  # for generating salt

# call local libraries

from opencc import OpenCC  # for Simplified Chinese to Traditional Chinese
import ToJyutping  # for Cantonese transcription
import ToMiddleChinese  # for Middle Chinese transcription

# Telegram bot

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ParseMode
from aiogram.utils.exceptions import MessageCantBeDeleted
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

`/ar` Translate to Arabic
`/en` Translate to English
`/es` Translate to Spanish
`/fr` Translate to French
`/ja` Translate to Japanese
`/ru` Translate to Russian
`/th` Translate to Thai
`/zh` Translate to Chinese

`/cmn` Translate to Mandarin (from Cantonese)
`/yue` Translate to Cantonese

`/och` Text labeling by Middle Chinese
`/yue_jyut` Text labeling by Cantonese pronunciation (Jyutping)

You can see a full list of commands [here](https://github.com/ayaka14732/trans/blob/main/commands.txt) (extremely long!).
If I am not working properly, please [report an issue](https://github.com/ayaka14732/trans) to my developers.'''

# Baidu translate

def md5(s):
	return hashlib.md5(s.encode('utf-8')).hexdigest()

def format_error_code(error_code):
	default_descr = 'Error: error code ' + error_code + '. Please contact the manager.'
	return \
		{ '54003': 'Error: Access frequency is limited. Please reduce your calling frequency.'
		, '54004': 'Error: The account balance is insufficient. Please contact the manager to recharge the account.'
		, '54005': 'Error: Long requests are too frequent. Please reduce the sending frequency of long queries and try again in 3 seconds.'
		, '58002': 'Error: The service is currently down. Please contact the manager to start the service.'
		}.get(error_code, default_descr)

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

# initialize

logging.basicConfig(level=logging.INFO)

traditionalize = OpenCC('s2hk').convert

# initialize bot

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# handle help command

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
	await message.reply(GREETINGS, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

# register command handler

def register_handler(command, f):
	dp.register_message_handler(f, commands=[command])
	dp.register_edited_message_handler(f, commands=[command])

# register Baidu translator

def create_translator(lang):
	async def f(message: Message):
		if message.reply_to_message:
			text = message.reply_to_message.text
		else:
			text = message.get_args()

		if text:
			text = await translate(text, lang)
			await message.reply(text)
	return f

register_handler('af', create_translator('afr'))
register_handler('ak', create_translator('aka'))
register_handler('am', create_translator('amh'))
register_handler('an', create_translator('arg'))
register_handler('ar', create_translator('ara'))
register_handler('as', create_translator('asm'))
register_handler('ay', create_translator('aym'))
register_handler('az', create_translator('aze'))
register_handler('ba', create_translator('bak'))
register_handler('be', create_translator('bel'))
register_handler('bg', create_translator('bul'))
register_handler('bi', create_translator('bis'))
register_handler('bn', create_translator('ben'))
register_handler('br', create_translator('bre'))
register_handler('bs', create_translator('bos'))
register_handler('ca', create_translator('cat'))
register_handler('co', create_translator('cos'))
register_handler('cs', create_translator('cs'))
register_handler('cv', create_translator('chv'))
register_handler('cy', create_translator('wel'))
register_handler('da', create_translator('dan'))
register_handler('de', create_translator('de'))
register_handler('dv', create_translator('div'))
register_handler('el', create_translator('el'))
register_handler('en', create_translator('en'))
register_handler('eo', create_translator('epo'))
register_handler('es', create_translator('spa'))
register_handler('et', create_translator('est'))
register_handler('eu', create_translator('baq'))
register_handler('fa', create_translator('per'))
register_handler('ff', create_translator('ful'))
register_handler('fi', create_translator('fin'))
register_handler('fo', create_translator('fao'))
register_handler('fr', create_translator('fra'))
register_handler('fy', create_translator('fry'))
register_handler('ga', create_translator('gle'))
register_handler('gl', create_translator('glg'))
register_handler('gn', create_translator('grn'))
register_handler('gu', create_translator('guj'))
register_handler('gv', create_translator('glv'))
register_handler('ha', create_translator('hau'))
register_handler('he', create_translator('heb'))
register_handler('hi', create_translator('hi'))
register_handler('hr', create_translator('hrv'))
register_handler('ht', create_translator('ht'))
register_handler('hu', create_translator('hu'))
register_handler('hy', create_translator('arm'))
register_handler('ia', create_translator('ina'))
register_handler('id', create_translator('id'))
register_handler('ig', create_translator('ibo'))
register_handler('io', create_translator('ido'))
register_handler('is', create_translator('ice'))
register_handler('it', create_translator('it'))
register_handler('iu', create_translator('iku'))
register_handler('ja', create_translator('jp'))
register_handler('jv', create_translator('jav'))
register_handler('ka', create_translator('geo'))
register_handler('kg', create_translator('kon'))
register_handler('kk', create_translator('kaz'))
register_handler('kl', create_translator('kal'))
register_handler('km', create_translator('hkm'))
register_handler('kn', create_translator('kan'))
register_handler('ko', create_translator('kor'))
register_handler('kr', create_translator('kau'))
register_handler('ks', create_translator('kas'))
register_handler('ku', create_translator('kur'))
register_handler('kw', create_translator('cor'))
register_handler('ky', create_translator('kir'))
register_handler('la', create_translator('lat'))
register_handler('lb', create_translator('ltz'))
register_handler('lg', create_translator('lug'))
register_handler('ln', create_translator('lin'))
register_handler('lo', create_translator('lao'))
register_handler('lt', create_translator('lit'))
register_handler('lv', create_translator('lav'))
register_handler('mg', create_translator('mg'))
register_handler('mh', create_translator('mah'))
register_handler('mi', create_translator('mao'))
register_handler('mk', create_translator('mac'))
register_handler('ml', create_translator('mal'))
register_handler('mr', create_translator('mar'))
register_handler('ms', create_translator('may'))
register_handler('mt', create_translator('mlt'))
register_handler('my', create_translator('bur'))
register_handler('ne', create_translator('nep'))
register_handler('nl', create_translator('nl'))
register_handler('no', create_translator('nor'))
register_handler('ny', create_translator('nya'))
register_handler('oc', create_translator('oci'))
register_handler('oj', create_translator('oji'))
register_handler('om', create_translator('orm'))
register_handler('or', create_translator('ori'))
register_handler('os', create_translator('oss'))
register_handler('pa', create_translator('pan'))
register_handler('pl', create_translator('pl'))
register_handler('ps', create_translator('pus'))
register_handler('pt', create_translator('pt'))
register_handler('qu', create_translator('que'))
register_handler('rm', create_translator('roh'))
register_handler('ro', create_translator('rom'))
register_handler('ru', create_translator('ru'))
register_handler('rw', create_translator('kin'))
register_handler('sa', create_translator('san'))
register_handler('sc', create_translator('srd'))
register_handler('sd', create_translator('snd'))
register_handler('se', create_translator('sme'))
register_handler('si', create_translator('sin'))
register_handler('sk', create_translator('sk'))
register_handler('sl', create_translator('slo'))
register_handler('sm', create_translator('sm'))
register_handler('sn', create_translator('sna'))
register_handler('so', create_translator('som'))
register_handler('sq', create_translator('alb'))
register_handler('sr', create_translator('srp'))
register_handler('st', create_translator('sot'))
register_handler('sv', create_translator('swe'))
register_handler('sw', create_translator('swa'))
register_handler('ta', create_translator('tam'))
register_handler('te', create_translator('tel'))
register_handler('tg', create_translator('tgk'))
register_handler('th', create_translator('th'))
register_handler('ti', create_translator('tir'))
register_handler('tk', create_translator('tuk'))
register_handler('tl', create_translator('tgl'))
register_handler('tr', create_translator('tr'))
register_handler('ts', create_translator('tso'))
register_handler('tt', create_translator('tat'))
register_handler('tw', create_translator('twi'))
register_handler('uk', create_translator('ukr'))
register_handler('ur', create_translator('urd'))
register_handler('uz', create_translator('uzb'))
register_handler('ve', create_translator('ven'))
register_handler('vi', create_translator('vie'))
register_handler('wa', create_translator('wln'))
register_handler('wo', create_translator('wol'))
register_handler('xh', create_translator('xho'))
register_handler('yi', create_translator('yid'))
register_handler('yo', create_translator('yor'))
register_handler('zh', create_translator('cht'))
register_handler('zu', create_translator('zul'))
register_handler('ace', create_translator('ach'))
register_handler('ang', create_translator('eno'))
register_handler('arq', create_translator('arq'))
register_handler('ast', create_translator('ast'))
register_handler('bal', create_translator('bal'))
register_handler('bem', create_translator('bem'))
register_handler('bho', create_translator('bho'))
register_handler('byn', create_translator('bli'))
register_handler('ceb', create_translator('ceb'))
register_handler('chr', create_translator('chr'))
register_handler('cnh', create_translator('hak'))
register_handler('cnr', create_translator('mot'))
register_handler('crh', create_translator('cri'))
register_handler('csb', create_translator('kah'))
register_handler('fur', create_translator('fri'))
register_handler('grc', create_translator('gra'))
register_handler('haw', create_translator('haw'))
register_handler('hil', create_translator('hil'))
register_handler('inh', create_translator('ing'))
register_handler('jbo', create_translator('loj'))
register_handler('kab', create_translator('kab'))
register_handler('kok', create_translator('kok'))
register_handler('lzh', create_translator('wyw'))
register_handler('mai', create_translator('mai'))
register_handler('mus', create_translator('cre'))
register_handler('nap', create_translator('nea'))
register_handler('nqo', create_translator('nqo'))
register_handler('nso', create_translator('ped'))
register_handler('pap', create_translator('pap'))
register_handler('sco', create_translator('sco'))
register_handler('shn', create_translator('sha'))
register_handler('szl', create_translator('sil'))
register_handler('tet', create_translator('tet'))
register_handler('tlh', create_translator('kli'))
register_handler('zza', create_translator('zaz'))

# special treatment for some Baidu translate commands

@dp.message_handler(commands=['yue'])
@dp.edited_message_handler(commands=['yue'])
async def translate_yue(message: Message):
	if message.reply_to_message:
		text = message.reply_to_message.text
	else:
		text = message.get_args()

	if text:
		text = await translate(text, 'yue')
		text = traditionalize(text)
		text = text.replace('系', '係')  # 係 is more commonly used in Cantonese
		await message.reply(text)

@dp.message_handler(commands=['cmn'])
@dp.edited_message_handler(commands=['cmn'])
async def translate_cmn(message: Message):
	if message.reply_to_message:
		text = message.reply_to_message.text
	else:
		text = message.get_args()

	if text:
		text = await translate(text, 'cht', src='yue')
		await message.reply(text)

# register translate functions in local libraries

def create_transformer(trans):
	async def f(message: Message):
		if message.reply_to_message:
			text = message.reply_to_message.text
		else:
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
