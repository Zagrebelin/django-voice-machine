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

month_names = [
    'января', 'февраля', "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "декабря"
]

hours_in_day = [
    (6, 7),
    (12, 13),
    (17, 18)
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://yandex.ru/pogoda/perm/details?lat=58.023361&lon=56.016228'
        rsp = requests.get(url)
        doc = fromstring(rsp.text)

        dd_days = doc.xpath("//dt[contains(@class, 'forecast-details__day')]")
        today = timezone.now()
        for dd_day in dd_days:
            day = int(dd_day.xpath(".//*[@class='forecast-details__day-number']/text()")[0])
            month = dd_day.xpath(".//*[@class='forecast-details__day-month']/text()")[0]
            month = month_names.index(month)+1
            if month == today.month:
                year = today.year
            elif month == 1 and today.month == 12:
                year = today.year + 1
            dd_weather = dd_day.xpath("./following-sibling::dd[1]")[0]
            print("\n", day, month, year)
            trs = dd_weather.xpath(".//tr[@class='weather-table__row']")
            for hours, tr in zip(hours_in_day, trs):
                temps = map(int, tr.xpath(".//div[contains(@class, 'weather-table__temp')]//span[@class='temp__value']/text()"))
                desc = tr.xpath(".//td[contains(@class, 'weather-table__body-cell_type_condition')]/text()")[0]
                wind = {
                    'speed': tr.xpath(".//span[@class='wind-speed']/text()"),
                    'direction': tr.xpath(".//div[@class='weather-table__wind-direction']/abbr/@title")
                }
                if wind['speed']:
                    wind['speed'] = int(wind['speed'][0].split(',')[0])
                    wind['direction'] = wind['direction'][0].split(':')[1]
                else:
                    wind['speed'] = 0
                    wind['direction'] = ''
                for hour, temp in zip(hours, temps):
                    when = datetime.datetime(year, month, day, hour, 0, 0)
                    when = timezone.make_aware(when, timezone=timezone.get_default_timezone())
                    models.Weather.objects.update_or_create(when=when,
                                                            defaults={'temperature': temp, 'description': desc,
                                                                      'wind': wind})
