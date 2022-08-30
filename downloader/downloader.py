import yt_dlp
from pathlib import Path




# Проверка на наличие ссылок в .txt документе.
async def exist_links(tgid):
    urls = []
    with open(str(Path(str(Path.cwd()), 'user_txt', f'{tgid}.txt')), "r") as file:
        for line in file:
            if ('https://youtu.be/' in line) and (line != r'\n'):
                urls.append(line.strip())

    if urls:
        for i in range(len(urls)):
            if len(urls) == 1:
                return False
            else:
                return True
    else:
        return False


# Получение количества url в .txt документе.
def get_count_url(tgid):
    list_url = []
    path_to_txt = str(Path(str(Path.cwd()), 'user_txt', f'{tgid}.txt'))
    with open(path_to_txt, "r") as file:
        for url in file:
            if ('https://youtu.be/' in url) and (url != r'\n'):
                list_url.append(url)
        count_urls = len(list_url)
    return count_urls


# Скачивание видеороликов в папку yt, текстовым методом
exodus_dwn = []
def ytb(tgid, quality):
    global exodus_dwn
    try:
        path_to_txt = str(Path(str(Path.cwd()), 'user_txt', f'{tgid}.txt'))
        prefix = 1

        with open(path_to_txt, "r") as file:
            for url in file:
                if ('https://youtu.be/' in url) and (url != r'\n'):
                    ydl_opts = {
                        'format_sort': [f'res:{quality}', 'ext:mp4:m4a'],
                        'outtmpl': f'{str(Path(str(Path.cwd()), "yt", f"{tgid}_{prefix}"))}.%(ext)s'
                    }
                    prefix += 1
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        try:
                            ydl.download([url.rstrip().strip()])
                            exodus_dwn.append(True)
                        except:
                            exodus_dwn.append(False)
                            print('[ОШИБКА СКАЧИВАНИЯ] /downloader.py/line 56')
    except Exception as _ex:
        print(_ex)

# Возвращение результата из потока
async def return_exodus_dwn():
    return exodus_dwn

# Очищение списка потока
async def clear_exodus_dwn():
    exodus_dwn.clear()


# Скачивание видеороликов в папку yt методом ссылки
def ytb_link(link, tgid, quality):
    ydl_opts = {
        'format_sort': [f'res:{quality}', 'ext:mp4:m4a'],
        'outtmpl': f'{str(Path(str(Path.cwd()), "yt", f"{tgid}_lnk"))}.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except:
            exodus_dwn.append(False)
        else:
            exodus_dwn.append(True)


# Скачивание mp3 - дорожки из видео в папку yt
def ytb_mp3(link, tgid):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{str(Path(str(Path.cwd()), "yt", f"{tgid}_aud"))}.mp3'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except:
            exodus_dwn.append(False)
        else:
            exodus_dwn.append(True)
