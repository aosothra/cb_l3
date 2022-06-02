import logging
import os
import traceback

import telegram
from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from bot_utils import TelegramLogHandler, detect_intent_texts


log = logging.getLogger(__file__)


def on_start(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте, задавайте вопросы.')


def on_message(update: Update, context: CallbackContext):
    text, _ = detect_intent_texts(
            project_id=os.getenv('GOOGLE_PROJECT_ID'),
            session_id=update.effective_chat.id,
            text=update.message.text,
            language_code='ru-RU'
            )
    
    update.message.reply_text(text)


def on_error(updat: object, context: CallbackContext):
    log.exception('An exception occured while handling an event.')


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.WARNING)
    log.setLevel(logging.ERROR)
    log.addHandler(
        TelegramLogHandler(env('ALARM_BOT_TOKEN'), env('ALARM_CHAT_ID'))
    )

    updater = Updater(env('TG_TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', on_start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, on_message))
    dispatcher.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
