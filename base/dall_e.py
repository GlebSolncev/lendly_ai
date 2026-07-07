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
    
    openai.api_key = settings.NEW_CHAT_GPT_KEY
    extra_prompts = ""


    response = openai.Image.create(
        model="dall-e-3",
        prompt= f"{prompt} {extra_prompts}",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    image_url = response['data'][0]['url']

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f'static/assets/dallegenerated/img/{timestamp}_{unique_id}.jpg'
    
    asyncio.run(save_image(image_url, filename))

    return f"{settings.DOMAIN_URL}{filename}"





    # image_url = 'http://127.0.0.1:8000/static/assets/dallegenerated/img/20240120175542_9bafa1e9.jpg'

    # return f"{image_url}"
   