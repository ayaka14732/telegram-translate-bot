from .baidu_api_status import BAIDU_API_STATUS

def _make_extra_commands() -> str:
    res = []

    for command, _, name, status in BAIDU_API_STATUS:
        if status == '1':
            res.append(f'`/{command}` Translate to {name}')

    return '\n'.join(res)

GREETING = f'''Meow! I am the translator bot. I can help you to do the following things.

*Translation:*

{_make_extra_commands()}
`/cmn` Translate to Mandarin (from Cantonese)
`/yue` Translate to Cantonese

*Transcription:*

`/furi` Add furigana to Japanese texts
`/och` Add Middle Chinese to Chinese texts (phonological description)
`/kyonh` Add Middle Chinese to Chinese texts (Koxyonh Romanization)
`/unt` Add Middle Chinese to Chinese texts (unt’s Reading Pronunciation of _Qieyun_)
`/tupa` Add Middle Chinese to Chinese texts (Tshet-uinh Phonetic Alphabet)
`/jyut` Add Jyutping to Cantonese texts
`/jyut_text` Add Jyutping to Cantonese texts (without Chinese characters)
`/jyut_ipa` Add IPA to Cantonese texts

*Others:*

`/del` Delete a previous message
`/help` Show this help
`/ping` Test the server connection

If I am not working properly, please [report an issue](https://github.com/ayaka14732/telegram-translate) to my developers.'''
