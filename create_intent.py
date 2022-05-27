import json
from environs import Env
from google.cloud import dialogflow
from google.cloud.dialogflow import Intent


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = Intent.Message.Text(text=[message_texts])
    message = Intent.Message(text=text)
    print(message)
    intent = Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()

    with open('questions.json', 'r', encoding='utf-8') as intents_file:
        intents_to_add = json.load(intents_file)
    
    for name, content in intents_to_add.items():
        create_intent('moonlit-grail-296914', name, content['questions'], content['answer'])


if __name__ == '__main__':
    main()