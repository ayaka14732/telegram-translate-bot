<a href="https://t.me/suginatransbot"><img src="avartar.jpeg" height="200px" align="right"/></a>

# telegram-translate

Telegram translation bot [@suginatransbot](https://t.me/suginatransbot)

## Develop

Create a bot by talking to [BotFather](https://t.me/botfather).

Register for [Baidu translate API](https://fanyi-api.baidu.com/).

## Run

Set the following environment variables in `.env`:

- `BOT_TOKEN`
- `BAIDU_APP_ID`
- `BAIDU_APP_KEY`
- `FURIGANA_API_URL`

Run:

```sh
python main.py
```

## Docker

```sh
git clone --depth=1 https://github.com/ayaka14732/furigana-server.git
```

You don't need to set `FURIGANA_API_URL` because it is managed by Docker Compose.

```sh
docker compose up -d
```

Update:

```sh
git pull
docker compose up -d --build
```
