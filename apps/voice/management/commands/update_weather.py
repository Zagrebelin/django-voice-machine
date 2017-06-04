import json
import datetime
import re
from io import StringIO
import csv

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

import requests
from lxml.html import fromstring

from ... import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = self.fetch()
        for item in data['list']:
            when = datetime.datetime.utcfromtimestamp(item['dt'])
            when2 = timezone.make_aware(when, timezone=timezone.utc)
            temp = int(item['main']['temp'])
            desc = ' или '.join(w['description'] for w in item['weather'])
            wind = ''
            models.Weather.objects.get_or_create(when=when2,
                                                 defaults={'temperature': temp, 'description': desc, 'wind': wind})

    def parse_row(self, tr):
        pass

    def fetch_x(self):
        return json.load(open('we.json'))

    def fetch(self):
        url = 'http://api.openweathermap.org/data/2.5/forecast?q=Perm,ru&appid=1df91491ea999dfa1ba79dbb41c8a0ad&lang=ru&units=metric'
        html = requests.get(url)
        data = html.json()
        return data
