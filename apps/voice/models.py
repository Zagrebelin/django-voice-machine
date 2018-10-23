import datetime

from django.db import models
from django.template import Context, Template
from django.utils import timezone

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
        return qs


def list_to_choices(*items):
    return [(item, item) for item in items]


class ScheduleItem(models.Model):
    use_holiday = models.BooleanField()
    use_workday = models.BooleanField()
    use_monday = models.BooleanField(default=True)
    use_tuesday = models.BooleanField(default=True)
    use_wednesday = models.BooleanField(default=True)
    use_thursday = models.BooleanField(default=True)
    use_friday = models.BooleanField(default=True)
    use_saturday = models.BooleanField(default=True)
    use_sunday = models.BooleanField(default=True)

    voice_type = models.CharField(max_length=50, choices=list_to_choices('primary', 'secondary', 'random'),
                                  default='primary')
    voice_emotion = models.CharField(max_length=50, choices=list_to_choices('neutral', 'evil', 'good'),
                                     default='neutral')

    time = models.TimeField()
    message = models.TextField(help_text='Возможные замены: {{time}}, {{date}}, {{weekday}}.')
    order = models.IntegerField(default=0)

    objects = ScheduleItemManager()

    @property
    def rendered_message(self):
        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        t = Template(self.message)
        context = {
            'date': humanize.date_as_string(today),
            'time': humanize.time_as_string(today),
            'weekday': humanize.weekday_as_string(today),
            'weather_today': humanize.weather_for_day(Weather.objects.for_morning(today),
                                                      Weather.objects.for_day(today),
                                                      Weather.objects.for_evening(today)),
            'weather_tomorrow': humanize.weather_for_day(Weather.objects.for_morning(tomorrow),
                                                         Weather.objects.for_day(tomorrow),
                                                         Weather.objects.for_evening(tomorrow))
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


class WeatherManager(models.Manager):
    def for_morning(self, dt: datetime.datetime):
        return self.for_hour_range(dt, 5, 10)

    def for_day(self, dt: datetime.datetime):
        return self.for_hour_range(dt, 11, 16)

    def for_evening(self, dt: datetime.datetime):
        return self.for_hour_range(dt, 16, 20)

    def for_hour_range(self, dt: datetime.datetime, from_hour: int, to_hour: int):
        d1 = timezone.make_aware(dt.replace(hour=from_hour, minute=0, second=0, microsecond=0))
        d2 = timezone.make_aware(dt.replace(hour=to_hour, minute=0, second=0, microsecond=0))
        qs = super().get_queryset()
        qs = qs.filter(when__range=(d1, d2))
        return qs


class Weather(models.Model):
    when = models.DateTimeField(unique=True)
    wind = models.CharField(max_length=200)
    temperature = models.IntegerField()
    description = models.CharField(max_length=200)

    objects = WeatherManager()

    def __str__(self):
        return str(self.when)


class RenderedScheduleItem(models.Model):
    when = models.DateTimeField()
    file = models.FileField()
    order = models.IntegerField()
    class Meta:
        ordering = ['order']