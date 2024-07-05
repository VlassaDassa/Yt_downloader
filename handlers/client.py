import asyncio
import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from pathlib import Path
from threading import Thread

from create_yt_downloader import bot
from keyboard import client_kb as cl_kb
from downloader import downloader as dwn
from telethon_bot.telethon_bot import send_video_to_bot
from database.sqlite_db import Database
import config as cfg





db = Database(cfg.path_to_db)


async def start(message: types.Message):
    mes_text = '<b>Привет 👋</b>\n' \
               'Этот бот предназначен для скачивания видео с YouTube\n' \
               'В качество до <b>1080p</b>\n' \
               '<b>Бесплатно!</b>'
    await message.answer(mes_text, parse_mode='HTML', reply_markup=cl_kb.choice_service)
    status = await db.get_status_download(message.from_user.id)
    count = await db.get_count_file(message.from_user.id)
    try:
        status[0]
    except:
        await db.set_status_download(message.from_user.id, 'inactive')
    try:
        count[0]
    except:
        await db.add_file(message.from_user.id, '0')


# Отключает стейты, удаляет файлы, перебрасывает на начальные кнопки
async def menu(message: types.Message, state: FSMContext):
    await message.answer('Меню 💤', reply_markup=cl_kb.choice_service)
    await message.delete()
    if str(await state.get_state()) == 'FSM_yt_method:quality':
        if os.path.exists(str(Path(str(Path.cwd()), 'user_txt', f'{message.from_user.id}.txt'))):
            os.remove(str(Path(str(Path.cwd()), 'user_txt', f'{message.from_user.id}.txt')))
    await state.finish()




# Выбор способа
async def youtube_downloader(message: types.Message):
    status = await db.get_status_download(message.from_user.id)
    if status[0] == 'inactive':
        mes_text = '<b>Выберите способ</b>\n' \
                   '• <b>Ссылкой</b> - вы просто кидаете ссылку и мы отправляем вам файл видео\n' \
                   '• <b>Текстовым файлом</b> - на каждой строчке обычного блокнота размещаете ссылку и отправляете его нам, все видео по ссылкам оттуда будут скачены\n' \
                   '[ВАЖНО] Текстовый файл должен выглядеть так:'
        await message.answer(mes_text, parse_mode='HTML', reply_markup=cl_kb.choice_method_yt)
        image = open(str(Path(str(Path.cwd()), 'assets', 'inst.jpg')), 'rb')
        await bot.send_photo(message.from_user.id, image)
    else:
        await message.answer('<b>Дождитесь скачивания</b>', reply_markup=cl_kb.choice_service, parse_mode='HTML')


# Старт машины состояний
class FSM_yt_method(StatesGroup):
    method = State()
    quality = State()

async def yt_method_txt(message: types.Message):
    await message.answer('<b>Отлично</b>\n'
                         'Ждём от вас <i>.txt</i> файл',
                         reply_markup=cl_kb.menu, parse_mode='HTML')
    await FSM_yt_method.method.set()


# Получение текстового документа
async def yt_get_txt(message: types.Message, state: FSMContext):
    cur_count_file = await db.get_count_file(message.from_user.id)
    new_count_file = int(cur_count_file[0]) + 1
    await db.update_count_file(message.from_user.id, new_count_file)

    if message.content_type == 'document':
        if message.document.file_name.split('.')[-1] == 'txt':
            try:
                await message.document.download(destination=str(Path(str(Path.cwd()), 'user_txt', f'{message.from_user.id}.txt')))
            except Exception as _ex:
                print(_ex)
                await message.answer('Какая-то ошибка...', reply_markup=cl_kb.choice_service)
            else:
                if await dwn.exist_links(message.from_user.id):

                    await message.answer('<b>Отлично!</b>\n'
                                         'Выберите качество',
                                         reply_markup=cl_kb.quality, parse_mode='HTML')
                    await FSM_yt_method.quality.set()
                else:
                    await message.answer('Некоторые ссылки в файле неправильные\n'
                                         'Возможно в файле лишь одна ссылка, воспользуйтесь другим разделом',
                                         reply_markup=cl_kb.choice_service, parse_mode='HTML')

                    os.remove(str(Path(str(Path.cwd()), 'user_txt', f'{message.from_user.id}.txt')))
                    await state.finish()
        else:
            await message.answer('Пришлите файл с расширением <b>.txt</b>\n'
                                 'Файлы .docx, xlsx и прочие не подходят',
                                 parse_mode='HTML', reply_markup=cl_kb.choice_service)
            await state.finish()
    else:
        await message.answer('Пришлите документ', reply_markup=cl_kb.choice_service)
        await state.finish()


# Выбор качества и начало скачивания
async def yt_finish(message: types.Message, state: FSMContext):
    global collapse_mes_stick
    count_file = await db.get_count_file(message.from_user.id)
    if int(count_file[0]) > 1:
        await message.answer('Пришлите 1 документ', reply_markup=cl_kb.choice_service)
        if os.path.exists(str(Path(str(Path.cwd()), 'user_txt', f'{message.from_user.id}.txt'))):
            os.remove(str(Path(str(Path.cwd()), 'user_txt', f'{message.from_user.id}.txt')))
        await db.update_count_file(message.from_user.id, '0')
        await db.update_status_download(message.from_user.id, 'inactive')
        await state.finish()
    else:
        list_quality = ['1080p', '720p', '480p']
        if message.text in list_quality:
            quality = message.text.replace('p', '')
            await state.finish()
            await db.update_status_download(message.from_user.id, 'active')
            collapse_mes_stick = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')

            yt_downloader = Thread(target=dwn.ytb, args=(message.from_user.id, quality))
            yt_downloader.start()

            for i in range(100000000):
                if yt_downloader.is_alive():
                    await asyncio.sleep(3)
                else:
                    break

            exodus_dwn = await dwn.return_exodus_dwn()
            if exodus_dwn[0]:
                for prefix in range(1, int(dwn.get_count_url(message.from_user.id)) + 1):

                    data_dict = {
                        'path_file': str(Path(str(Path.cwd()), 'yt', f'{message.from_user.id}_{prefix}.mp4')),
                        'tgid': message.from_user.id,
                        'file_name': f'{message.from_user.id}_{prefix}.mp4',
                        'bot_name': cfg.BOT_NICKNAME
                    }

                    await send_video_to_bot(data_dict)
                    await state.finish()
            else:
                await message.answer('Ошибка скачивания, повторите позже', reply_markup=cl_kb.choice_service)
                await db.update_status_download(message.from_user.id, 'inactive')
                await state.finish()
                try:
                    await bot.delete_message(message.from_user.id, collapse_mes_stick.message_id)
                except:
                    pass
        else:
            await message.answer('Неверное качество', reply_markup=cl_kb.choice_service)
            await db.update_status_download(message.from_user.id, 'inactive')
            await state.finish()
        if os.path.exists(str(Path(str(Path.cwd()), 'user_txt', f'{message.from_user.id}.txt'))):
            os.remove(str(Path(str(Path.cwd()), 'user_txt', f'{message.from_user.id}.txt')))
        await dwn.clear_exodus_dwn()
    await db.update_count_file(message.from_user.id, '0')


# Получение видео от User agent и пересылка его изначальному пользователю
async def get_and_send_video(message: types.Message):
    if str(message.from_user.id) == cfg.ID_CLIENT:
        try:
            message.caption.split('_')[0]
        except:
            print('[ОШИБКА] User agent кинул видео без префикса')
        else:
            tgid = message.caption.split('_')[0]
            file_id = message.video.file_id
            if 'lnk' not in message.caption:
                prefix = message.caption.split('_')[1].split(':')[0]
                global progress_bar
                global stick_mes
                if int(prefix) == 1:
                    
                    try:
                        await bot.delete_message(tgid, collapse_mes_stick.message_id)
                    except:
                        pass
                    progress_bar = await bot.send_message(tgid, '<b>Прогресс скачивания</b>\n'
                                                                f'◻◻◻{prefix}/{dwn.get_count_url(tgid)}◻◻◻',
                                                                parse_mode='HTML')
                    stick_mes = await bot.send_sticker(tgid, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')
                elif (int(prefix) != 1) and (os.path.exists(str(Path(str(Path.cwd()), 'user_txt', f'{tgid}.txt')))):
                    await bot.edit_message_text('<b>Прогресс скачивания</b>\n'
                                                f'◻◻◻{prefix}/{dwn.get_count_url(tgid)}◻◻◻',
                                                tgid, progress_bar.message_id, parse_mode='HTML')
                else:
                    await bot.edit_message_text('<b>Прогресс скачивания</b>\n'
                                                f'◻◻◻{prefix}/{prefix}◻◻◻',
                                                tgid, progress_bar.message_id, parse_mode='HTML')

                await bot.send_video(tgid, file_id)
                if not os.path.exists(str(Path(str(Path.cwd()), 'user_txt', f'{tgid}.txt'))):
                    await bot.send_message(tgid, '<b>Скачивание завершено</b>\n'
                                                 f'{prefix}/{prefix}',
                                                  parse_mode='HTML', reply_markup=cl_kb.choice_service)
                    await db.update_status_download(tgid, 'inactive')
                    try:
                        await bot.delete_message(tgid, progress_bar.message_id)
                        await bot.delete_message(tgid, stick_mes.message_id)
                    except:
                        pass
                os.remove(str(Path(str(Path.cwd()), 'yt', f'{message.caption}.mp4')))
            else:
                await bot.send_message(tgid, '<b>Скачивание завершено</b>', reply_markup=cl_kb.choice_service, parse_mode='HTML')
                await bot.send_video(tgid, file_id)
                await db.update_status_download(tgid, 'inactive')
                try:
                    await bot.delete_message(tgid, collapse_mes_stick_lnk.message_id)
                except:
                    pass
                if os.path.exists(str(Path(str(Path.cwd()), 'yt', f'{tgid}_lnk.mp4'))):
                    os.remove(str(Path(str(Path.cwd()), 'yt', f'{tgid}_lnk.mp4')))
    else:
        await message.answer('Не нужно мне кидать видео :)')


# Начало работы машины состояний для метода "ссылкой"
class FSM_yt_link(StatesGroup):
    method = State()
    quality = State()

async def yt_method_link(message: types.Message):
    await message.answer('<b>Отлично</b>\n'
                         'Ждём от вас <i>ссылку</i>',
                         reply_markup=cl_kb.menu, parse_mode='HTML')
    await FSM_yt_link.method.set()


# Получение ссылки на скачивание
async def yt_get_link(message: types.Message, state: FSMContext):
    if 'https://youtu.be/' in message.text:
        if len(message.text.strip().rstrip()) == 28:
            async with state.proxy() as data:
                data['link'] = message.text
            await FSM_yt_link.quality.set()
            await message.answer('<b>Выберите качество ролика</b>', reply_markup=cl_kb.quality_lnk, parse_mode='HTML')
        else:
            await message.answer('Пришлите 1 ссылку', reply_markup=cl_kb.choice_service)
            await state.finish()
    else:
        await message.answer('Неверная ссылка', reply_markup=cl_kb.choice_service)
        await state.finish()


# Выбор качества и начало скачивания
async def yt_link_finish(message: types.Message, state: FSMContext):
    global collapse_mes_stick_lnk
    list_quality = ['1080p', '720p', '480p']
    if message.text in list_quality:
        async with state.proxy() as data:
            quality = message.text.replace('p', '')
            link = data['link']
            await db.update_status_download(message.from_user.id, 'active')
            collapse_mes_stick_lnk = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')
            start_download = Thread(target=dwn.ytb_link, args=(link, message.from_user.id, quality))
            start_download.start()

            for i in range(100000):
                if start_download.is_alive():
                    await asyncio.sleep(3)
                else:
                    break

            exodus = await dwn.return_exodus_dwn()
            if exodus[0]:
                data = {
                    'path_file': str(Path(str(Path.cwd()), 'yt', f'{message.from_user.id}_lnk.mp4')),
                    'file_name': f'{message.from_user.id}_lnk.mp4',
                    'tgid': message.from_user.id,
                    'bot_name': cfg.BOT_NICKNAME
                }

                await send_video_to_bot(data)
                await state.finish()
            else:
                await db.update_status_download(message.from_user.id, 'inactive')
                await state.finish()
                try:
                    await bot.delete_message(message.from_user.id, collapse_mes_stick.message_id)
                except:
                    pass
                await message.answer('<b>Ошибка при скачивании</b>', reply_markup=cl_kb.choice_service, parse_mode='HTML')
    else:
        if message.text == 'MP3':
            collapse_mes_stick_lnk = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')
            async with state.proxy() as data:
                start_download_mp3 = Thread(target=dwn.ytb_mp3, args=(data['link'], message.from_user.id))
                start_download_mp3.start()

                for i in range(100000):
                    if start_download_mp3.is_alive():
                        await asyncio.sleep(3)
                    else:
                        break

                exodus = await dwn.return_exodus_dwn()
                if exodus[0]:
                    await bot.delete_message(message.from_user.id, collapse_mes_stick_lnk.message_id)
                    await bot.send_audio(message.from_user.id, open(str(Path(str(Path.cwd()), 'yt', f'{message.from_user.id}_aud.mp3')), 'rb'))
                    os.remove(str(Path(str(Path.cwd()), 'yt', f'{message.from_user.id}_aud.mp3')))
                else:
                    await db.update_status_download(message.from_user.id, 'inactive')
                    await state.finish()
                    try:
                        await bot.delete_message(message.from_user.id, collapse_mes_stick.message_id)
                    except:
                        pass
                    await message.answer('<b>Ошибка при скачивании</b>', reply_markup=cl_kb.choice_service,
                                         parse_mode='HTML')
                await dwn.clear_exodus_dwn()
        else:
            await message.answer('Неверное качество', reply_markup=cl_kb.choice_service)
            await state.finish()
            await db.update_status_download(message.from_user.id, 'inactive')






# Регистрация обработчиков
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], chat_type='private')
    dp.register_message_handler(menu, Text(equals="Меню 💤"), state="*", chat_type='private')
    dp.register_message_handler(youtube_downloader, Text(equals='YouTube'), chat_type='private')

    # yt with txt
    dp.register_message_handler(yt_method_txt, Text(equals='Текстовым файлом 🗎'), chat_type='private', state=None)
    dp.register_message_handler(yt_get_txt, content_types=['document'], state=FSM_yt_method.method, chat_type='private')
    dp.register_message_handler(yt_finish, state=FSM_yt_method.quality, chat_type='private')
    dp.register_message_handler(get_and_send_video, content_types=['video'], chat_type='private')

    # yt with one link
    dp.register_message_handler(yt_method_link, Text(equals='Ссылкой ✏'), chat_type='private', state=None)
    dp.register_message_handler(yt_get_link, state=FSM_yt_link.method, chat_type='private')
    dp.register_message_handler(yt_link_finish, state=FSM_yt_link.quality, chat_type='private')


