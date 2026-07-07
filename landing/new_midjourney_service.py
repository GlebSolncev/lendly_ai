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


class NewMidjourneyService:
    _api_key = settings.MIDJOURNEY_API_KEY
    _BASE_URL = 'https://api.thenextleg.io/v2/'
    _AUTH_HEADERS = {
        "Authorization": f"Bearer 746dfb8d-2a11-4034-90e1-53d363347c87",
        "Content-Type": "application/json",
    }

    def fetch_to_completion(self,message_id, retry_count, max_retry=200):
        image_res = requests.get(f"{self._BASE_URL}message/{message_id}", headers=self._AUTH_HEADERS)
        image_response_data = image_res.json()

        print(image_response_data)
        if image_response_data["progress"] == "incomplete":
            raise Exception("Image generation failed")

        if retry_count > max_retry:
            raise Exception("Max retries exceeded")

        if image_response_data["progress"]:
            # print("---------------------")
            print(f'Progress: {image_response_data["progress"]}%')
            # print("---------------------")
            return image_response_data


        # sleep(5000)
        return self.fetch_to_completion(message_id, retry_count + 1)

    def main(self,prompt=""):
        # Generate the image
        image_res = requests.post(
            f"{self._BASE_URL}imagine", headers=self._AUTH_HEADERS, json={"msg": prompt}
        )
        image_response_data = image_res.json()
        print("\n=====================")
        print("IMAGE GENERATION MESSAGE DATA")
        print(image_response_data)
        print("=====================")

        return image_response_data
        # end


    
    # def _make_progress_request(self, messageId: str) -> MidjourneyProgressDTO:
    #     url = self._BASE_URL + 'message/' + messageId
    #     try:
    #         response = requests.request('GET', url, headers=self._base_request_headers)
    #     except requests.HTTPError as error:
    #         raise MidjourneyException('Midjourney API error!' + str(error))
    #     data = response.json()
    #     progress = data.get('progress', False)
    #     if progress == 0 or progress != False:
    #         if data['progress'] < 100:
    #             return MidjourneyProgressDTO(data['progress'])
    #         else:
    #             return MidjourneyProgressDTO(data['progress'], data['response']['imageUrls'][0])
    #     else:
    #         raise MidjourneyException('Midjourney API error! Invalid response ')

    # def poll_img(self, messageId: str) -> str:
    #     failed_responses = 0
    #     error = ""
    #     while failed_responses < 3:
    #         try:
    #             dto = self._make_progress_request(messageId)
    #             if dto.percentage < 100:
    #                 time.sleep(2)
    #                 continue
    #             else:
    #                 return dto.url
    #         except MidjourneyException as err:
    #             failed_responses += 1
    #             error = str(err)
    #     raise MidjourneyException('Midjourney API error!' + error)


new_midjourney_service = NewMidjourneyService()
