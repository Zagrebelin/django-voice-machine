from django.core.management import BaseCommand

import yandex_voice

from ...models import ScheduleItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        items = ScheduleItem.objects.for_date().order_by('order').all()
        filenames = []
        for item in items:
            text = item.rendered_message
            parts = text.split('.')
            for part in parts:
                filenames.append(yandex_voice.generate_mp3(part, item.voice_type, item.voice_emotion))
        if filenames:
            print(filenames)
