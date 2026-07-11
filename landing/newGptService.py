import openai
from django.conf import settings


class newGptService:

    @staticmethod
    def sendPrompt(prompt, maxT):
        client = openai.OpenAI(api_key=settings.NEW_CHAT_GPT_KEY)

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=maxT
        )

        data = response.choices[0].message.content

        data_without_linebreaks = data.replace('\n', '').replace('\r', '').replace('"', '')

        return data_without_linebreaks