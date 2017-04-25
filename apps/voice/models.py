import datetime

from django.db import models
from django.template import Context, Template

import humanize


class Holiday(models.Model):
    date = models.DateField()
    year = models.IntegerField()

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')


class ScheduleItemManager(models.Manager):
    weekdaynames = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def for_date(self, dt: datetime.datetime = None):
        if not dt:
            dt = datetime.datetime.now()
        dt = dt.replace(second=0, microsecond=0)
        is_holiday = Holiday.objects.filter(date=dt.date()).count() > 0
        qs = super().get_queryset()
        if is_holiday:
            qs = qs.filter(use_holiday=True)
        else:
            qs = qs.filter(use_workday=True)
        weekday_field = 'use_' + self.weekdaynames[dt.weekday()]
        qs = qs.filter(**{weekday_field: True})
        qs = qs.filter(time=dt.time())
        print(str(qs.query))
        return qs


def list_to_choices(*items):
    return [(item, item) for item in items]


class ScheduleItem(models.Model):
    use_holiday = models.BooleanField()
    use_workday = models.BooleanField()
    use_monday = models.BooleanField()
    use_tuesday = models.BooleanField()
    use_wednesday = models.BooleanField()
    use_thursday = models.BooleanField()
    use_friday = models.BooleanField()
    use_saturday = models.BooleanField()
    use_sunday = models.BooleanField()

    voice_type = models.CharField(max_length=50, choices=list_to_choices('primary', 'secondary'), default='primary')
    voice_emotion = models.CharField(max_length=50, choices=list_to_choices('neutral', 'evil', 'good'),
                                     default='neutral')

    time = models.TimeField()
    message = models.TextField(help_text='Возможные замены: {{time}}, {{date}}, {{weekday}}.')
    order = models.IntegerField()

    objects = ScheduleItemManager()

    @property
    def rendered_message(self):
        dt = datetime.datetime.now()
        t = Template(self.message)
        context = {
            'date': humanize.date_as_string(dt),
            'time': humanize.time_as_string(dt),
            'weekday': humanize.weekday_as_string(dt)
        }
        ret = t.render(Context(context))
        return ret

    @property
    def display_date(self):
        wd = []
        if self.use_monday:
            wd.append('пн')
        if self.use_tuesday:
            wd.append('вт')
        if self.use_wednesday:
            wd.append('ср')
        if self.use_thursday:
            wd.append('чт')
        if self.use_friday:
            wd.append('пт')
        if self.use_saturday:
            wd.append('сб')
        if self.use_sunday:
            wd.append('вс')

        if not wd:
            return 'Никогда'
        if len(wd) == 7:
            a1 = 'В любой день'
        else:
            a1 = 'В ' + ' '.join(wd)

        if self.use_workday and not self.use_holiday:
            a2 = 'если это рабочий день'
        elif not self.use_workday and self.use_holiday:
            a2 = 'если это выходной или праздник'
        elif self.use_workday and self.use_holiday:
            a2 = 'если это выходной, праздник или рабочий день'
        else:
            return 'Никогда'

        if len(wd) == 7 and self.use_workday and self.use_holiday:
            return 'Каждый день'

        return f'{a1}, {a2}'
