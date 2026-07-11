import openai
from django.conf import settings
import logging

logger = logging.getLogger('app_api')


def get_chat_response(prompt, max_tokens=150):
    # Вызываем OpenAI прямо из модуля — так IDE гарантированно всё увидит
    client = openai.OpenAI(api_key=settings.CHAT_GPT_KEY)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()