import datetime

import flask_admin as admin
from flask import Flask
from flask_admin.contrib import sqla

import models

app = Flask('voice-machine')

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample_db_2.sqlite'
app.config['SQLALCHEMY_ECHO'] = True


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
    next_minute = datetime.datetime.now()+datetime.timedelta(minutes=1)
    return get_strings_date(next_minute)


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
    #models.db.init_app(app)
    #with app.app_context():
    #    models.db.create_all()

    admin = admin.Admin(app, name='Voice Machine', template_mode='bootstrap3')
    admin.add_view(ScheduleItemAdmin(models.ScheduleItem, models.session))
    admin.add_view(sqla.ModelView(models.Holiday, models.session))

    app.run()
