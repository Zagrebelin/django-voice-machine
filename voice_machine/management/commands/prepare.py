from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

from ...models import ScheduleItem, RenderedScheduleItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... import tools
        dt = (datetime.now() + timedelta(minutes=1)).replace(second=0, microsecond=0)
        items = ScheduleItem.objects.for_date(dt).order_by('order').all()
        filenames = tools.download(items)
        for order, filename in enumerate(filenames):
            RenderedScheduleItem.objects.create(when=dt, file=filename, order=order)
