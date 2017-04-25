from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

from ...models import ScheduleItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... import tools
        dt = datetime.now() + timedelta(minutes=1)
        items = ScheduleItem.objects.for_date(dt).order_by('order').all()
        print(items)
        tools.download(items)
