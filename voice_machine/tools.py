import random
import typing
from hashlib import md5
from typing import Generator

import requests
from django.conf import settings
from django.core.files.storage import default_storage

from . import models


def talk(items: typing.List[models.ScheduleItem]):
    filenames = download(items)
    if filenames:
        settings.MP3_PLAYER(filenames)


def download(items: typing.List[models.ScheduleItem], dt):
    voices = getattr(settings, 'YANDEX_SPEECH_VOICES', {'primary': 'oksana'})
    primary_voice = voices['primary']
    storage = default_storage

    filenames = []
    urls = []
    for item in items:
        text = item.render(dt)
        parts = text.split('.')
        for part in parts:
            if item.voice_type == 'random':
                voice = random.choice(list(voices.values()))
            else:
                voice = voices.get(item.voice_type, primary_voice)
            filename = md5(f'{voice} {item.voice_emotion} {part}'.encode()).hexdigest() + '.mp3'

            if not storage.exists(filename):
                file = storage.open(filename, mode='wb')
                for chunk in get_mp3_content(part, voice, item.voice_emotion):
                    file.write(chunk)
                file.close()
            filenames.append(filename)
            urls.append(storage.url(filename))

    return filenames, urls


def get_mp3_content(msg: str, voice: str, emotion: str = 'neutral') -> Generator[bytes, None, None]:
    url = 'https://tts.voicetech.yandex.net/generate'
    data = {
        'text': msg,
        'format': 'mp3',
        'lang': 'ru-RU',
        'speaker': voice,
        'key': settings.YANDEX_SPEECH_API_KEY,
        'emotion': emotion
    }
    rsp = requests.get(url, params=data, stream=True)
    for data in rsp.iter_content(chunk_size=4096):
        yield data
