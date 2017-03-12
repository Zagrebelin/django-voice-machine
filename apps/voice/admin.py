from django.contrib import admin

from . import models
admin.site.register(models.Holiday, list_filter=['year'])
admin.site.register(models.ScheduleItem, list_display=['message', 'display_date', 'time', 'order'])

# Register your models here.
