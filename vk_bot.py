import os
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

from dialogflow_wrap import detect_intent_texts

def echo(event, vk_api):
    text = detect_intent_texts(
        project_id=os.getenv('GOOGLE_PROJECT_ID'),
        session_id=event.user_id,
        text=event.text,
        language_code='ru-RU'
        )
    
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()

    vk_session = vk.VkApi(token=env('VK_ACCESS_TOKEN'))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == '__main__':
    main()