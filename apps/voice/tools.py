import random
import typing
from hashlib import md5

from django.conf import settings
from django.core.files.storage import get_storage_class, DefaultStorage, default_storage

import yandex_voice
from . import models


def talk(items: typing.List[models.ScheduleItem]):
    filenames = download(items)
    if filenames:
        settings.MP3_PLAYER(filenames)


def download(items: typing.List[models.ScheduleItem]):
    primary_voice = settings.YANDEX_SPEECH_VOICES['primary']
    storage = default_storage

    filenames = []
    for item in items:
        text = item.rendered_message
        parts = text.split('.')
        for part in parts:
            if item.voice_type == 'random':
                voice = random.choice(list(settings.YANDEX_SPEECH_VOICES.values()))
            else:
                voice = settings.YANDEX_SPEECH_VOICES.get(item.voice_type, primary_voice)
            filename = md5(f'{voice} {item.voice_emotion} {part}'.encode()).hexdigest() + '.mp3'

            if not storage.exists(filename):
                file = storage.open(filename, mode='wb')
                for chunk in yandex_voice.get_mp3_content(part, voice, item.voice_emotion):
                    file.write(chunk)
                file.close()
            filenames.append(filename)

    return filenames
