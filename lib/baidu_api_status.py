def _get_baidu_api_status():
    res = []

    with open('baidu_api_status.csv', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            command, lang_code, name, status = line.rstrip('\n').split(',')
            res.append((command, lang_code, name, status))

    return res

BAIDU_API_STATUS = _get_baidu_api_status()
