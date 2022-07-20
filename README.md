<a href="https://t.me/suginatransbot"><img src="avartar.jpeg" height="200px" align="right"/></a>

# Telegram translation bot

Telegram translation bot [@suginatransbot](https://t.me/suginatransbot)

## Develop

Create a bot by talking to [BotFather](https://t.me/botfather).

Register for [Baidu translate API](https://fanyi-api.baidu.com/).

## Run

Set the following environment variables in `.env`:

- `BOT_TOKEN`
- `BAIDU_APP_ID`
- `BAIDU_APP_KEY`

Run:

```sh
python main.py
```

Alternatively, pass the environment variables to Docker in the command:

```sh
docker run -d \
  -e BOT_TOKEN=<BOT_TOKEN> \
  -e BAIDU_APP_ID=<BAIDU_APP_ID> \
  -e BAIDU_APP_KEY=<BAIDU_APP_KEY> \
  telegram-translate
```
