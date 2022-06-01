import json
from argparse import ArgumentParser

from environs import Env
from dialogflow_wrap import create_intent


def main():
    env = Env()
    env.read_env()

    parser = ArgumentParser()
    parser.add_argument('path_to_json', help='fullpath to JSON with intents to create')
    args = parser.parse_args()

    with open(args.path_to_json, 'r', encoding='utf-8') as intents_file:
        intents_to_add = json.load(intents_file)
    
    for name, content in intents_to_add.items():
        create_intent('moonlit-grail-296914', name, content['questions'], content['answer'])


if __name__ == '__main__':
    main()