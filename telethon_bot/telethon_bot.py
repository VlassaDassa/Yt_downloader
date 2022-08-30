import os

from telethon import TelegramClient
from dotenv import load_dotenv, find_dotenv



load_dotenv(find_dotenv())

# Создание сессии User agent и отправка видео боту при его появлении в папке yt
async def send_video_to_bot(data: dict):
    entity = 'Yt_downloader'
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone = os.getenv('PHONE')
    client = TelegramClient(entity, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        # await client.send_code_request(phone)  # Раскомментировать при первом запуске
        await client.sign_in(phone, input('Enter code: '))
    await client.start()

    file_path = data['path_file']
    prefix = file_path.split('_')[-1].split('.')[0]
    file_name = data['file_name']
    chat_id = data['tgid']
    bot_name = data['bot_name']
    msg = await client.send_file(
                           str(bot_name),
                           file_path,
                           caption=f'{chat_id}_{prefix}',
                           file_name=str(file_name),
                           use_cache=False,
                           part_size_kb=512,
                           )

    await client.disconnect()
