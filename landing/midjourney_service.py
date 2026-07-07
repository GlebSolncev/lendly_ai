import time
from django.conf import settings
import requests
import json
from landing.models import Landing, LandingImage

class MidjourneyException(Exception):
    pass


class MidjourneyProgressDTO:
    def __init__(self, percentage: int, url = None):
        self.percentage = percentage
        self.url = url


def _get_img_count_by_template(template_name: str) -> int:
    if template_name == 'template_1.html':
        return 5
    if template_name == 'template_2.html':
        return 2
    if template_name == 'template_3.html':
        return 2


class MidjourneyService:
    _api_key = settings.MIDJOURNEY_API_KEY
    _BASE_URL = 'https://api.thenextleg.io/v2/'

    @property
    def _json_request_headers(self):
        headers = self._base_request_headers
        headers['Content-Type'] = 'application/json'
        return headers

    @property
    def _base_request_headers(self):
        return {'Authorization': 'Bearer ' + self._api_key}

    def _make_imagine_request(self, payload: str) -> str:
        url = self._BASE_URL + 'imagine'
        try:
            response = requests.request('POST', url, headers=self._json_request_headers, data=payload)
        except requests.HTTPError as error:
            raise MidjourneyException('Midjourney API error!')
        data = response.json()
        if data.get('success', False) and data.get('messageId', False):
            return data['messageId']
        else:
            raise MidjourneyException('Midjourney API error!')

    def img_by_prompt(self, prompt: str) -> str:
        payload = json.dumps({"msg": prompt})
        return self._make_imagine_request(payload)

    def img_2_img(self, img_url: str, prompt: str) -> str:
        payload = json.dumps({"msg": f"{img_url} {prompt}"})
        return self._make_imagine_request(payload)

    def _make_progress_request(self, messageId: str) -> MidjourneyProgressDTO:
        url = self._BASE_URL + 'message/' + messageId
        try:
            response = requests.request('GET', url, headers=self._base_request_headers)
        except requests.HTTPError as error:
            raise MidjourneyException('Midjourney API error!' + str(error))
        data = response.json()
        progress = data.get('progress', False)
        if progress == 0 or progress != False:
            if data['progress'] < 100:
                return MidjourneyProgressDTO(data['progress'])
            else:
                return MidjourneyProgressDTO(data['progress'], data['response']['imageUrls'][0])
        else:
            raise MidjourneyException('Midjourney API error! Invalid response ')

    def poll_img(self, messageId: str) -> str:
        failed_responses = 0
        error = ""
        while failed_responses < 3:
            try:
                dto = self._make_progress_request(messageId)
                if dto.percentage < 100:
                    time.sleep(2)
                    continue
                else:
                    return dto.url
            except MidjourneyException as err:
                failed_responses += 1
                error = str(err)
        raise MidjourneyException('Midjourney API error!' + error)

    def generate_images(self, landing: Landing):
        img_count = _get_img_count_by_template(landing.template.template)
        images = []
        for i in range(1, img_count):
            image = LandingImage()
            image.landing = landing
            image.message_id = self.img_by_prompt(landing.company_description)
            image.save()
            images.append(image)
            time.sleep(1)
        for image in images:
            url = self.poll_img(image.message_id)
            image.url = url
            image.save()

midjourney_service = MidjourneyService()
