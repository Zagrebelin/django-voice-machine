from django.core.management import BaseCommand

from ...models import ScheduleItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... import tools
        items = ScheduleItem.objects.for_date().order_by('order').all()
        print(items)
        tools.talk(items)
