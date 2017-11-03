import datetime
import re
from io import StringIO
import csv

from django.core.management.base import BaseCommand, CommandError

import requests
from lxml.html import fromstring

from ... import models


class Command(BaseCommand):
    """ Update list of holidays from http://data.gov.ru/opendata/7708660670-proizvcalendar"""
    def handle(self, *args, **options):
        rsp = requests.get('http://data.gov.ru/opendata/7708660670-proizvcalendar')
        doc = fromstring(rsp.text)
        csv_url = doc.xpath("//a[contains(@href, 'UTF-8') and " \
                            "contains(@href, '-structure-') and " \
                            "contains(@href, '/data-')]/@href")[0]
        csv_txt = requests.get(csv_url).text
        csv_file = StringIO(csv_txt)
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)
        ret = []
        this_year = datetime.datetime.now().year
        for line in reader:
            year = int(line['Год/Месяц'])
            if year < this_year:
                continue
            models.Holiday.objects.filter(year=year).delete()
            month_names = 'Январь Февраль Март Апрель Май Июнь Июль Август Сентябрь Октябрь Ноябрь Декабрь'.split()
            for month_num, month_name in enumerate(month_names):
                days = line[month_name]
                days = list(map(int, re.findall('\d+(?!\*)', days)))
                dates = (datetime.datetime(year=year, month=month_num + 1, day=day) for day in days)
                hds = [models.Holiday(year=year, date=date) for date in dates]
                models.Holiday.objects.bulk_create(hds)
                if year == this_year:
                    ret += ['%d %s' % (day, month_name) for day in days]

        return ', '.join(ret)
