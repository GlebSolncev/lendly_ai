import base64
from datetime import datetime
import uuid
import os
import re
import requests
import json
import asyncio
import aiohttp
from django.conf import settings


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

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-image-1-mini",
        "prompt": f"{prompt} {extra_prompts}",
        "size": "1024x1024",
        "quality": "low",
        # "n": 1
    }

    api_response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload
    )

    # Проверяем успешность ответа от OpenAI
    # if api_response.status_code == 200:
    #     response_data = api_response.json()
    #
    #     # Безопасно вытаскиваем URL
    #     try:
    #         image_url = response_data['data'][0]['url']
    #     except (KeyError, IndexError):
    #         raise KeyError(f"OpenAI вернул успешный статус 200, но структура данных изменилась: {response_data}")
    # else:
    #     # Если статус не 200, принудительно выводим ошибку, чтобы сразу увидеть её на экране дебага
    #     raise Exception(f"OpenAI API Error (Status {api_response.status_code}): {api_response.text}")
    #
    # # Логика генерации имени локального файла
    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # unique_id = str(uuid.uuid4())[:8]
    # filename = f'static/assets/dallegenerated/img/{timestamp}_{unique_id}.jpg'
    #
    # # Запускаем асинхронный таск скачивания в синхронной вьюхе Django
    # asyncio.run(save_image(image_url, filename))
    if api_response.status_code == 200:
        response_data = api_response.json()

        # Безопасно достаем base64 строку вместо url
        try:
            image_base64 = response_data['data'][0]['b64_json']
        except (KeyError, IndexError):
            raise KeyError(f"OpenAI вернул успешный статус 200, но в ключе b64_json пусто: {response_data}")
    else:
        # Если статус не 200, принудительно выводим ошибку, чтобы сразу увидеть её на экране дебага
        raise Exception(f"OpenAI API Error (Status {api_response.status_code}): {api_response.text}")

        # Генерируем имя локального файла
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f'static/assets/dallegenerated/img/{timestamp}_{unique_id}.jpg'

    # ШАГ 2: Декодируем base64 в чистые байты картинки
    image_bytes = base64.b64decode(image_base64)

    # ШАГ 3: Синхронно сохраняем файл на диск (aiohttp и asyncio больше не нужны!)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(image_bytes)

    print(f"Image decoded and saved successfully as {filename}")

    # Возвращаем полный путь до картинки
    return f"{settings.DOMAIN_URL}{filename}"