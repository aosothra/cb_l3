from google.cloud.dialogflow import SessionsClient, TextInput, QueryInput


def detect_intent_texts(project_id, session_id, text, language_code):
    '''Returns the result of detect intent with text as input.'''

    session_client = SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = TextInput(text=text, language_code=language_code)
    query_input = QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )

    return (
        response.query_result.fulfillment_text, 
        response.query_result.intent.is_fallback
    )