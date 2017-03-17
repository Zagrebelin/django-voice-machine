from django.core.management import BaseCommand
from django.conf import settings

import yandex_voice

from ...models import ScheduleItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        primary_voice = settings.YANDEX_SPEECH_VOICES['primary']
        items = ScheduleItem.objects.for_date().order_by('order').all()
        filenames = []
        for item in items:
            text = item.rendered_message
            parts = text.split('.')
            for part in parts:
                voice = settings.YANDEX_SPEECH_VOICES.get(item.voice_type, primary_voice)
                filenames.append(yandex_voice.generate_mp3(part, voice, item.voice_emotion))
        if filenames:
            settings.MP3_PLAYER(filenames)
