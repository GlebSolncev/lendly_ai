import openai
from django.conf import settings
import uuid
from landing.models import Landing
import logging
logger = logging.getLogger('app_api')


class ChatGPTService:
    _api_key = settings.CHAT_GPT_KEY

    def __init__(self):
        openai.api_key = self._api_key

    def _send_request(self, prompt, max_tokens=50, fallback=''):
        response = openai.Completion.create(
            model='gpt-3.5-turbo-instruct',
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            n=5,
        )
        choices = []
        for index, choice in enumerate(response['choices']):
            if not choice['text']:
                choice['text'] = fallback
            
            # choices.append(choice['text'].replace('\n', '').replace('.', '').replace('!', '').replace('"', ''))

            random_str = str(uuid.uuid4()).split('-')[0]  

            choice_obj = {
                'id': f'{index + 1}_{random_str}',
                'text': choice['text'].replace('\n', '').replace('.', '').replace('!', '').replace('"', '')
            }

            choices.append(choice_obj)


        # choices = list(dict.fromkeys(choices))

        return choices

    def get_prompt(self, field, landing: Landing, company):
        prompts = {
            'hero': f'Create a title for website. Without welcome. Without company name. One unique short laconic sentence. {company}',
            'hero_long': f'Create a description for website. One unique laconic sentence. The text should not look like "{landing.hero}". {company}',
            'services': f'Create a text core services of website. ONLY one unique description sentence. The text should not contain "Core Services:" The text should be in format "Service title:Service description" {company}',
            'about_us': f'Create a text about the website. ONLY one unique description sentence. The text should be in format "About title:About description" {company}',
            'statistics': f'Create a text of statistics of website. ONLY one unique statistic. Value must be ONLY integer. The text should not contain "Statistic:". The text should be in format "Statistic title:Statistic value" {company}',
            'testimonials': f'Create a testimonial of website. ONLY one unique testimonial. {company}',
            'cta': f'Create a CTA for website. One unique short laconic sentence. {company}',
            'cta_long': f'Create a CTA description for website. CTA: {landing.cta}. {company}',
        }
        return prompts[field]

    def generate_landing(self, landing: Landing, fields=None):

        if fields==None:
            companyName = landing.get_only_company_name()['text']
        else:
            companyName = landing.get_company_name()['text']



    #    get_only_company_name

        company = f'Company name: {companyName}, company description: {landing.company_description}'

        print(company)
     
        multiple = ['services', 'statistics', 'about_us', 'testimonials']

        if not fields:
            fields = ['hero', 'hero_long', 'services', 'statistics', 'about_us', 'testimonials', 'cta', 'cta_long']

        for field in fields:
            prompt = self.get_prompt(field, landing, company)
            value = self._send_request(prompt, fallback= companyName)
            if field in multiple:
                landing.__setattr__(field, value[:4])
                landing.__setattr__(field + '_list', value)
                texts = value
                valued_data = value[:4]


            else:
                landing.__setattr__(field, value[0])
                landing.__setattr__(field + '_list', value)
                texts = value
                valued_data = value[0]
        landing.save()
   

        if fields:
            valued_data_arr = []

            valued_data_arr.append(valued_data)

            return texts, valued_data_arr
          


chat_gpt_service = ChatGPTService()
