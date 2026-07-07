import openai
from django.conf import settings
import logging
logger = logging.getLogger('app_api')

def get_chat_response(prompt, max_tokens=150):
    openai.api_key = settings.CHAT_GPT_KEY
    response = openai.Completion.create(
        model='gpt-3.5-turbo-instruct',
        prompt=prompt,
        max_tokens=max_tokens
    )    
    return response.choices[0].text