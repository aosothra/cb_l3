# cb_l3 - Helper chat-bots

This project implements smart conversation bots ([VK](https://vk.com/club211678335), [Telegram](https://t.me/gov_support_chat_bot)) for initial customer support of made-up company called "Game of Verbs"

The whole "smart" thing works through [DialogFlow](https://cloud.google.com/dialogflow/docs) platform on Google Cloud Services.

You may create your own smart bots using provided utility scripts.

## Installation and Environment setup

You must have Python3 installed on your system.

You may use `pip` (or `pip3` to avoid conflict with Python2) to install dependencies.
```
pip install -r requirements.txt
```
It is strongly advised to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for project isolation.

This script uses `.env` file in root folder to store variables necessary for operation. So, do not forget to create one!

Inside your `.env` file you can specify following settings:

| Key | Type | Required by | Description |
| - | - | - | - |
| `GOOGLE_PROJECT_ID` | `str` | `create_intent.py`, `tg_bot.py`, `vk_bot.py` | Unique identifier of your DialogFlow project within Google Cloud Services.
| `GOOGLE_APPLICATION_CREDENTIALS` | `str` | `create_intent.py`, `tg_bot.py`, `vk_bot.py` | Path to JSON file with authentication credentials for Google Cloud Services.
| `TG_TOKEN` | `str` | `tg_bot.py` | Your Telegram bot API token to handle conversations in Telegram. 
| `VK_ACCESS_TOKEN` | `str` | `vk_bot.py` | Your VK token for group messages access to handle conversations in VK.
| `ALARM_BOT_TOKEN` | `str` | `tg_bot.py`, `vk_bot.py` | Telegram API token for error notification.
| `ALARM_CHAT_ID` | `int` | `tg_bot.py`, `vk_bot.py` | Telegram chat guid as notification recipient.

For proper operation of the bot you will need to set up and configure DialogFlow powered Google project. You can follow [official guidelines](https://cloud.google.com/dialogflow/es/docs/quick/setup) for initial setup and agent creation. Make sure to go over **authentication set up** in order to create [service account](https://cloud.google.com/dialogflow/es/docs/quick/setup#sa-create) and [acquire private keys](https://cloud.google.com/dialogflow/es/docs/quick/setup#auth-env)

You will need to set up DialogFlow Agent in order to handle flow of the conversation. Follow steps of the [official documentation](https://cloud.google.com/dialogflow/es/docs/quick/build-agent) to get the gist of it. 

Once you've figured it out, you may use provided utility `create_intent.py`.

If you do not know how to acquire Telegram Bot token, you can follow official guidelines [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

If you do not know how to acquire VK group access token, you can find it in [here](https://dev.vk.com/api/community-messages/getting-started#Получение%20ключа%20доступа%20в%20настройках%20сообщества).

## Basic usage

Use `tg_bot.py` to start Telegram bot:

```
py tg_bot.py 
```

Use `vk_bot.py` to start VK Group bot:

```
py vk_bot.py 
```

In order to create DialogFlow Agent Intents in bulk, use `create_intent.py` script. It requires one positional argument to specify path to a JSON file, that holds data for new intents in the following schema:

```JavaScript
{
    "intent display name": {
        "questions": [
            "Question phrasing 1",
            "Question phrasing 2",
            ... ,
            "Question phrasing N"
        ],
        "answer": "Fullfillment text."
    },
    ...
}
```
Once you have your JSON at hand, use following command:

```
py create_intent.py <path_to_json>
```

## Project goals

This project was created for educational purposes as part of [dvmn.org](https://dvmn.org/) Backend Developer course.