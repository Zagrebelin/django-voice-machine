from django.contrib import admin
from django.contrib.admin import ModelAdmin

from . import models
from . import forms

class ScheduleItemAdmin(ModelAdmin):
    list_display = ['message', 'display_date', 'time', 'order']

    def get_form(self, request, obj=None, **kwargs):
        return forms.ScheduleItemForm

admin.site.register(models.Holiday, list_filter=['year'])
admin.site.register(models.ScheduleItem, ScheduleItemAdmin)

# Register your models here.
