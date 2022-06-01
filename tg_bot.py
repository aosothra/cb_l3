import logging
import os

from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow_wrap import detect_intent_texts


log = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте, задавайте вопросы.')


def echo(update: Update, context: CallbackContext):
    text = detect_intent_texts(
            project_id=os.getenv('GOOGLE_PROJECT_ID'),
            session_id=update.effective_chat.id,
            text=update.message.text,
            language_code='ru-RU'
            )
    
    update.message.reply_text(text)


def error_handler(updat: object, context: CallbackContext):
    #TODO: Implement proper error logging
    pass


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.WARNING)
    log.setLevel(logging.ERROR)

    updater = Updater(env('TG_TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()