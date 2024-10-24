import os
from MukeshAPI import api
from PIL import Image
import io
import random
import asyncio
import data.db_helper as db

async def get_random_text_part(bio_text):
    bio_parts = bio_text.split(';\n')
    return random.choice(bio_parts)

async def init_db():
    database_bot = db.DatabaseBot("data//db_helper.db")
    await database_bot.connect()
    return database_bot

async def generate_image(user_id,thread_num,promt,path_img):
    try:
        '''async with db.DatabaseBot("DataBase/bd.db") as db_bot:
            phone_info = await db_bot.phone_info(user_id)'''
        '''desc = await get_random_text_part(phone_info[38])'''
        '''new_desc = str(desc).replace(';', '')'''
        tt = "in the center"
        # Get the image from the API
        response = api.ai_image(f"{promt}. {tt}")
        # Save the image to a file
        with open(f"temp/mukesh_{user_id}_{thread_num}.jpg", 'wb') as f:
            f.write(response)
        # Open the image using Pillow
        with Image.open(io.BytesIO(response)) as img:
            # Crop the image to a width of 720 pixels, keeping the center
            width, height = img.size
            left = (width - 720) / 2
            top = 0
            right = (width + 720) / 2
            bottom = height
            img_cropped = img.crop((left, top, right, bottom))

            # Resize the image to a height of 1080 pixels while maintaining aspect ratio
            img_resized = img_cropped.resize((720, 1080), Image.LANCZOS)

            # Save the modified image
            img_resized.save(f"{path_img}")

        os.remove(f"temp/mukesh_{user_id}_{thread_num}.jpg")

        return path_img

    except Exception as e:
        print(e)
        return False