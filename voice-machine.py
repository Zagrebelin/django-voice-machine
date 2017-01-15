import datetime
import csv
from io import StringIO
import re

from lxml.html import fromstring
import flask_admin as admin
from flask import Flask
from flask_admin.contrib import sqla
import requests

import models

app = Flask('voice-machine')


class ScheduleItemAdmin(sqla.ModelView):
    column_filters = ('use_holiday',
                      'use_workday',
                      'use_monday',
                      'use_tuesday',
                      'use_wednesday',
                      'use_thursday',
                      'use_friday',
                      'use_saturday',
                      'use_sunday',)
    column_labels = {'use_holiday': 'Выходные',
                     'use_workday': 'Будни',
                     'use_monday': 'Понедельник',
                     'use_tuesday': 'Вторник',
                     'use_wednesday': 'Среда',
                     'use_thursday': 'Четверг',
                     'use_friday': 'Пятница',
                     'use_saturday': 'Суббота',
                     'use_sunday': 'Воскресение',
                     'holiday_or_weekday': 'Рабочие дни или выходные',
                     'weekdays': 'Дни недели'
                     }
    column_list = ('time', 'message', 'order', 'holiday_or_weekday', 'weekdays')
    column_default_sort = 'time'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/now')
def get_strings_now():
    today = datetime.datetime.now()
    return get_strings_date(today)


@app.route('/next_minute')
def get_strings_next_minute():
    next_minute = datetime.datetime.now() + datetime.timedelta(minutes=1)
    return get_strings_date(next_minute)


@app.route('/update_holidays')
def update_holidays():
    session = models.Session(autocommit=True)
    rsp = requests.get('http://data.gov.ru/opendata/7708660670-proizvcalendar')
    doc = fromstring(rsp.text)
    csv_url = \
    doc.xpath("//a[contains(@href, 'UTF-8') and contains(@href, '-structure-') and contains(@href, '/data-')]/@href")[0]
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
        session.query(models.Holiday).filter_by(year=year).delete()
        month_names = 'Январь Февраль Март Апрель Май Июнь Июль Август Сентябрь Октябрь Ноябрь Декабрь'.split()
        for month_num, month_name in enumerate(month_names):
            days = line[month_name]
            days = list(map(int, re.findall('\d+', days)))
            dates = (datetime.datetime(year=year, month=month_num + 1, day=day) for day in days)
            hds = (models.Holiday(year=year, date=date) for date in dates)
            session.add_all(hds)
            if year == this_year:
                ret += ['%d %s' % (day, month_name) for day in days]

    return ', '.join(ret)


def get_strings_date(dt):
    weekday = dt.strftime('%A').lower()
    time = datetime.time(hour=dt.hour, minute=dt.minute)
    date = dt.date()
    holiday = models.session.query(models.Holiday).filter_by(date=date).count()
    parts = models.session.query(models.ScheduleItem)
    parts = parts.filter_by(time=time)
    parts = parts.filter_by(**{'use_%s' % weekday: 1})
    if holiday:
        parts = parts.filter_by(use_holiday=1)
    else:
        parts = parts.filter_by(use_workday=1)
    parts = parts.order_by(models.ScheduleItem.order)
    parts = parts.values('message')
    txt = ' '.join(p[0] for p in parts)
    return txt


if __name__ == '__main__':
    # models.db.init_app(app)
    # with app.app_context():
    #    models.db.create_all()

    admin = admin.Admin(app, name='Voice Machine', template_mode='bootstrap3')
    admin.add_view(ScheduleItemAdmin(models.ScheduleItem, models.session))
    admin.add_view(sqla.ModelView(models.Holiday, models.session))

    app.run()
