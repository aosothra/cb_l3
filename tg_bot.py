import logging
import os

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


log = logging.getLogger(__file__)


def detect_intent_texts(project_id, session_id, text, language_code):
    '''Returns the result of detect intent with text as input.'''

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )

    return response.query_result.fulfillment_text


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте, задавайте вопросы.')


def echo(update: Update, context: CallbackContext):
    text = detect_intent_texts(
            os.getenv('GOOGLE_PROJECT_ID'),
            update.effective_chat.id,
            update.message.text,
            'ru-RU'
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