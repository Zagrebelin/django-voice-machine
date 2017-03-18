from django.core.management import BaseCommand
from django.core.management import CommandParser

from ...models import ScheduleItem
from ...tools import  talk


class Command(BaseCommand):
    def add_arguments(self, parser:CommandParser):
        parser.add_argument('--voice', action='store', choices=['primary', 'secondary'], default='primary')
        parser.add_argument('--emotion', action='store', choices=['neutral', 'evil', 'good'], default='neutral')
        parser.add_argument('text_to_speech', nargs='*')

    def handle(self, voice, emotion, text_to_speech, *a, **kw):
        item = ScheduleItem(voice_emotion=emotion, voice_type=voice, message=text_to_speech)
        talk([item])