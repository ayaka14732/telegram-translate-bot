<a href="https://t.me/suginatransbot"><img src="avatar.jpeg" height="200px" align="right"/></a>

# Telegram Translation Bot

This repository contains the source code for the Telegram translation bot [@suginatransbot](https://t.me/suginatransbot)

## Development

Create a bot by talking to [BotFather](https://t.me/botfather).

Register for the [Baidu Translate API](https://fanyi-api.baidu.com/).

## Run

Set the following environment variables in the `.env` file:

- `BOT_TOKEN`
- `BAIDU_APP_ID`
- `BAIDU_APP_KEY`
- `FURIGANA_API_URL`

Then run:

```sh
python main.py
```

## Docker

Clone the Furigana Server repository:

```sh
git clone https://github.com/ayaka14732/furigana-server.git
cd furigana-server
git checkout f0dbf1001ec6a863cda08f50eb294d776f0ec8e0
```

When using Docker Compose, you do not need to set `FURIGANA_API_URL`, as it is managed internally by the Compose network.

Start the services:

```sh
docker compose up -d
```

To update:

```sh
git pull
docker compose up -d --build
```
