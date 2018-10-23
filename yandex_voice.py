from hashlib import md5
from typing import Generator
import os

from django.conf import settings

import requests


def generate_mp3(msg: str, voice: str, emotion: str = 'neutral', avoid_cache=False) -> str:
    cache_dir = settings.YANDEX_SPEECH_CACHE_PATH
    os.makedirs(cache_dir, exist_ok=True)
    filename = md5(f'{voice} {emotion} {msg}'.encode()).hexdigest() + '.mp3'
    filename = os.path.join(cache_dir, filename)
    if not avoid_cache and os.path.exists(filename):
        return filename
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
    with open(filename, 'wb') as f:
        for data in rsp.iter_content(chunk_size=4096):
            f.write(data)
    return filename


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
