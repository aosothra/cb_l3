import logging
import os
import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from bot_utils import detect_intent_texts, TelegramLogHandler


log = logging.getLogger(__file__)


def handle_message(event, vk_api):
    text, is_fallback = detect_intent_texts(
        project_id=os.getenv('GOOGLE_PROJECT_ID'),
        session_id=event.user_id,
        text=event.text,
        language_code='ru-RU'
        )
    
    if is_fallback:
        vk_api.messages.markAsRead(peer_id=event.user_id)
        return
    
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.WARNING)
    log.setLevel(logging.ERROR)
    log.addHandler(
        TelegramLogHandler(env('ALARM_BOT_TOKEN'), env('ALARM_CHAT_ID'))
    )

    vk_session = vk.VkApi(token=env('VK_ACCESS_TOKEN'))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                handle_message(event, vk_api)
            except Exception:
                log.exception('An exception occured while handling a message.')


if __name__ == '__main__':
    main()