import logging
import os
import traceback

import telegram
from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow_utils import detect_intent_texts


log = logging.getLogger(__file__)


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot = telegram.Bot(bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)

        self.bot.send_message(
            chat_id=self.chat_id,
            text=log_entry
        )


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
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    log.error(f'An exception occured while handling an event.\n{tb_string}')


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