from django.core.management.base import BaseCommand, CommandError

from ...models import ScheduleItem

class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... import tools
        items = ScheduleItem.objects.for_date().order_by('order').all()
        tools.download(items)
