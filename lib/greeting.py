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
`/och` Text labeling by Middle Chinese
`/och_kyonh` Text labeling by Middle Chinese (Koxyonh Romanization)
`/och_unt` Text labeling by Middle Chinese (unt’s Reading Pronunciation of _Qieyun_)
`/jyut` Text labeling by Cantonese pronunciation (Jyutping)
`/yue_ipa` Text labeling by Cantonese pronunciation (IPA)

*Others:*

`/del` Delete a previous message
`/help` Show help
`/ping` Test the server connection

If I am not working properly, please [report an issue](https://github.com/ayaka14732/trans) to my developers.'''
