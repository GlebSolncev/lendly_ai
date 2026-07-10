from datetime import datetime
import uuid , os, re, openai
from django.conf import settings

import json
import requests
from django.http import JsonResponse
import aiohttp
import asyncio

async def download_image(session, image_url, filename):
    async with session.get(image_url) as response:
        if response.status == 200:
            image_data = await response.read()
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as file:
                file.write(image_data)
            print(f"Image saved successfully as {filename}")
        else:
            print(f"Failed to download image. Status code: {response.status}")

async def save_image(image_url, filename):
    async with aiohttp.ClientSession() as session:
        await download_image(session, image_url, filename)


def dall_e(prompt):
    api_key = settings.NEW_CHAT_GPT_KEY
    extra_prompts = ""

    # Формируем заголовки для авторизации в API OpenAI
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Payload запроса с явным указанием dall-e-3
    payload = {
        "model": "dall-e-3",
        "prompt": f"{prompt} {extra_prompts}",
        "size": "1024x1024",
        "quality": "standard",
        "n": 1
    }

    # Делаем прямой POST-запрос к эндпоинту OpenAI
    api_response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload
    )

    # Проверяем успешность ответа от OpenAI
    if api_response.status_code == 200:
        response_data = api_response.json()
        image_url = response_data['data'][0]['url']
    else:
        raise Exception(f"OpenAI API Error: {api_response.text}")

    # Оставляем твою логику сохранения файла без изменений
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f'static/assets/dallegenerated/img/{timestamp}_{unique_id}.jpg'

    asyncio.run(save_image(image_url, filename))

    return f"{settings.DOMAIN_URL}{filename}"





    # image_url = 'http://127.0.0.1:8000/static/assets/dallegenerated/img/20240120175542_9bafa1e9.jpg'

    # return f"{image_url}"
   