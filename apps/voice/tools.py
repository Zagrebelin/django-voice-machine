import typing

from django.conf import settings
import yandex_voice
from . import models


def talk(items: typing.List[models.ScheduleItem]):
    filenames = download(items)
    print(filenames)
    if filenames:
        settings.MP3_PLAYER(filenames)


def download(items: typing.List[models.ScheduleItem]):
    primary_voice = settings.YANDEX_SPEECH_VOICES['primary']

    filenames = []
    for item in items:
        text = item.rendered_message
        parts = text.split('.')
        for part in parts:
            voice = settings.YANDEX_SPEECH_VOICES.get(item.voice_type, primary_voice)
            filenames.append(yandex_voice.generate_mp3(part, voice, item.voice_emotion))
    return filenames
