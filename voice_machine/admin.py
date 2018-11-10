from django.contrib import admin
from django.contrib.admin import ModelAdmin

from . import models
from . import forms

class ScheduleItemAdmin(ModelAdmin):
    list_display = ['message', 'display_date', 'time', 'order']
    ordering = ['time', 'order']
    list_filter = ['use_holiday', 'use_workday']
    
    def get_form(self, request, obj=None, **kwargs):
        return forms.ScheduleItemForm

admin.site.register(models.Holiday, list_filter=['year'])
admin.site.register(models.ScheduleItem, ScheduleItemAdmin)
admin.site.register(models.Weather)

# Register your models here.
