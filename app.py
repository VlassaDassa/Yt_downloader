from aiogram.utils import executor

from create_yt_downloader import dp
from handlers import client



async def on_startup(_):
    print('Бот вышел в онлайн\n')

    
client.register_handlers_client(dp)


def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
