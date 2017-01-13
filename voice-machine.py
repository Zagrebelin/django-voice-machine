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
    column_filters=('use_holiday',
                    'use_workday',
                    'use_monday',
                    'use_tuesday',
                    'use_wednesday',
                    'use_thursday',
                    'use_friday',
                    'use_saturday',
                    'use_sunday',)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/now')
def get_strings_now():
    today = datetime.datetime.now()
    weekday = today.strftime('%A').lower()
    parts = models.ScheduleItem.query
    parts = parts.filter_by(hour=today.hour, minute=today.minute)
    parts = parts.filter_by(**{'use_%s' % weekday: 1})
    parts = parts.order_by(models.ScheduleItem.order)
    parts = parts.values('message')
    txt = ' '.join(p[0] for p in parts)
    return txt


if __name__ == '__main__':
    models.db.init_app(app)
    with app.app_context():
        models.db.create_all()
    admin = admin.Admin(app, name='Voice Machine', template_mode='bootstrap3')
    admin.add_view(ScheduleItemAdmin(models.ScheduleItem, models.db.session))

    app.run()
