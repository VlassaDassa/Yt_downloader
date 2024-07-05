# Yt_downloader

## Функционал
- Скачивание видео с YouTube;
- 1080, 720, 480, mp3;
- Возможность закинуть файл с ссылками, для поочерёдной долгой загрузки;

## Стэк
- FFmpeg - объединение видео 1080p со звуковой дорожкой;
- Aiogram - Telegram Bot;
- Telethon - Для обхода ограничения, при котором бот не может отправлять сообщения больше чем 50мб;
- python==3.7.2

## Инструкция для запуска
Установить FFmpeg - [инструкция](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)

Создать Telegram client [здесь](https://my.telegram.org/apps)
```sh
python -m venv venv
venv\Scripts\activate
pip install -r .\requirements.txt
python app.py
```
В файле config.py, изменить переменные: BOT_NICKNAME и ID_CLIENT

Создать файл .env и заполнить новые переменные: API_ID, API_HASH, PHONE, TOKEN

PHONE в формате +7xxx

API_ID и API_HASH можно взять [здесь](https://my.telegram.org/apps)
TOKEN у @BotFather



