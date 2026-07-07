import openai
from django.conf import settings



openai.api_key = settings.NEW_CHAT_GPT_KEY


class newGptService:

    def sendPrompt(prompt, maxT):
        response = openai.Completion.create(
            model='gpt-3.5-turbo-instruct',
            prompt= prompt, 
            max_tokens=maxT
        )    
        data = response.choices[0].text
        data_without_linebreaks = data.replace('\n', '').replace('\r', '').replace('"', '')

        return data_without_linebreaks


# newGptService = newGptService()
